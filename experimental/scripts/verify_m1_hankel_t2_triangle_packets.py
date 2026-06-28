#!/usr/bin/env python3
"""Verify t=2 same-slope triangle packet lifts in the Hankel model.

Proof status: PROVED-LOCAL / EXACT FINITE VERIFICATION.

The previous t=2 verifier checks one-exchange edges.  This script checks the
next local shape: pairwise one-exchange triangles inside a fixed-slope fiber.
For the combined syndrome s=Syn(Y-lambda phi), a complement T is active when

    H_{2,j}(s) ell_T = 0.

Every pairwise one-exchange triangle of active complements is either a star or
a top packet:

* star triangles have a common (j-1)-core R and lift to H_{3,j-1}(s) ell_R=0;
* top triangles are contained in a common (j+1)-set U and lift to
  H_{1,j+1}(s) ell_U=0.

The script enumerates all syndrome vectors in small cases, including the first
genuine top-triangle case (F_7, k=2, t=2, j=2).

It also checks the core-plane classification.  For each (j-2)-core R, active
extensions T=R union {x,y} are solutions of two affine equations in
(sigma,pi)=(x+y,xy).  The consecutive Hankel form rules out non-fixed affine
lines in a fixed same-slope fiber: each core plane is empty, a point, a
fixed-root line, or the full lower-Hankel core plane H_{4,j-2}(s) ell_R=0.
Consequently every two-edge corner in the active one-exchange graph is either
a star corner covered by H_{3,j-1}, or a lower-core corner covered by
H_{4,j-2}.
At the component level, any nontrivial component without a lower-core corner
is contained in one star and is covered by H_{3,j-1}; every non-star component
contains a lower-core H_{4,j-2} witness.
The verifier also records the resulting component ledger: non-isolated active
complements are covered by one-row edge cores, and non-star components are
covered by lower-core witnesses.
Finally it checks the isolated-vertex criterion: an active complement is
isolated in the one-exchange graph exactly when every one-root deletion has a
nonzero H_{3,j-1} boundary vector.
It also records the resulting marked-boundary ledger j*|Iso| <= |B_rm|.
Combining the non-isolated and isolated ledgers, it checks the full active
support ledger

    j*|A| <= j*(n-j+1)*|E| + |B_rm|,

where E is the set of active one-exchange edge cores.
It also checks the sharper first-boundary incidence identity

    j*|A| = (n-j+1)*|E| + |B_rm|.

Root by root, it checks the fixed-root decomposition

    |A_x| = |Z_x| + |B_x|,

where A_x is the active fixed-root slice, Z_x is the zero-boundary core slice
available to x, and B_x is the root-marked boundary slice marked by x.
It then identifies A_x with the root-slice Hankel kernel for the difference
syndrome Delta_x s = (s_{i+1} - x s_i)_i.
Inside that kernel, the root-marked residual is checked to be exactly the
single-row nonzero slice H_{1,j-1}(s) ell_C != 0.
One-exchange edges inside each root-marked slice are checked to descend to
H_{tau+1,j-2}(Delta_x s) on their common lower core.
The remaining isolated vertices in those slices are checked by the analogous
nonzero lower-boundary criterion and ledger.
Finally, it checks the iterated fixed-root identity and the induced recursive
first-boundary ledger: multiplying a locator by prod_i (X-x_i) is the same as
applying the ordered root-difference operator Delta_{x_m}...Delta_{x_1} to the
syndrome, and the zero-boundary/root-marked incidence identity holds on each
difference rung.  It also checks the set-level filtration partition behind
that identity, and audits the induced first-zero stopping decomposition for
ordered fixed-root deletion paths.  The path audit records the resulting
first-zero/terminal ledger and reduces terminal flags to unordered bottom
root-difference supports up to the factorial ordering factor.  It also checks
that terminality is exactly a zero-free chain of first-row boundary scalars.
The terminal zero-free flags are then checked again by the exact deletion-tree
recursion whose nonzero outgoing edges are these same scalar cuts; multiflag
terminal supports must contain an explicit branching vertex in this tree.
Every pair of nonzero outgoing edges is checked to force a two-mode lower
boundary vector on the core obtained by deleting both roots.
More generally, the verifier checks the all-exit sparse mode-packet formula
at every terminal branch vertex.
Whenever the packet length is long enough, it also checks the nonzero
moment-Hankel determinant certificate for that sparse packet.
It checks that applying the locator of any subset of branch modes peels off
exactly those modes, with no proper-subset zero collapse.
It also recovers the unique monic minimal annihilator from visible moments and
checks that it is exactly the branch-mode locator.
At the maximal rank-visible boundary, where only 2m-1 moments are available,
it searches for equal-size support aliases and checks that every such alias is
disjoint from the true branch-mode set and satisfies the expected
kernel-weight amplitude criterion.  It also checks the equivalent terminal
branch-scalar form: a disjoint candidate Z aliases a mode set Y exactly when
c_y prod_{z in Z}(y-z) is independent of y in Y.
In the full-domain boundary case n=2m over roots of unity, it checks the
equivalent root-linear amplitude test a_y/y = constant on Y.
It records the resulting labeled support profile for root-linear packets.
More generally, it records the boundary fiber-size histogram and checks the
matching bound fiber_size <= floor(n/m).
It also reports the ambient labeled sparse-packet capacity
binom(n,m)(p-1)^m for each boundary mode size encountered in the scan.
For all visible terminal mode packets, it reports the same labeled capacity by
mode size as the packet-type ledger.
Finally, it checks that an anchored packet label reconstructs its branch core
and all first-row exit scalars.
It also counts, syndrome by syndrome, how many times the same unanchored
visible sparse-packet label is produced by terminal deletion-tree branch
vertices.
It checks that every terminal packet is the direct Hankel image of its
collapsed anchor base A=X union R; repeated labels with distinct anchor bases
therefore force a lower-degree anchor-base kernel relation.
It also audits the one-exchange refinement: an adjacent anchor-base collision
forces the common (|A|-1)-core into the same Hankel kernel.
It checks the reversible split-support certificate: for collapsed anchor
base A and packet modes Y, the total support A union Y is active and every
one-mode deletion has the expected nonzero root-marked boundary vector.
Conversely, it checks that those root-marked split-boundary scalars reconstruct
the anchor-base sparse packet.
For a fixed active total split support, it audits the exact factorization of
certificates by nonzero root-marked exits: every marked subset reconstructs
the corresponding anchor packet, and every produced certificate uses such a
marked subset.
It also audits the full marked-exit cube of each produced total support:
every nonempty subset of marked exits is a lossless sparse packet face over
the complementary anchor.
For the canonical unmarked core S\\M(S), it audits the resulting full-marked
support fibers: below the boundary they are unique, while boundary fibers are
matching-bounded.
It also audits the dual zero cube: every nonempty subset of unmarked roots
descends to a deeper zero Hankel kernel.
The marked and unmarked cubes are also audited together: deleting unmarked
roots first shifts the row depth additively and rescales the marked sparse
packet without loss.
After such an unmarked deletion, it audits that the marked set is exactly
preserved and the remaining unmarked roots stay unmarked.
It also checks the canonical-core simple-pole lift: after deleting all marked
exits, every unmarked core root gives the same sparse packet with amplitudes
divided by the corresponding simple pole y-u.
At the boundary marked size t+1, this extra simple-pole row recovers the
marked locator whenever the unmarked core is nonempty, so the verifier checks
that only empty-core boundary fibers can have matching ambiguity.
For the remaining empty-core endpoint, it records the produced full-marked
boundary fibers and, in the full-domain case n=2(t+1), checks that nontrivial
produced pairs are root-linear complements.
More generally, it checks moment-complete canonical cores: if the unmarked
core has at least r-t roots for r marked exits, mixed faces supply enough
moments to recover the marked support uniquely.
For the remaining moment-short cores, it checks the deficit-packing rule:
with d=r-t-|U|>0, two distinct marked frontiers over the same unmarked core
cannot share d marked roots, hence each fiber obeys the elementary d-subset
packing bound.
Equivalently, it audits the deficit-anchor injection: a fixed unmarked core
and any d marked roots determine the whole marked frontier.
For each such anchor, it also checks that filtering the syndrome by the
anchor locator gives a squarefree residual Hankel kernel whose monic
annihilator is exactly the remaining marked locator.
It enumerates the whole squarefree residual-kernel fiber for produced
anchors and checks the standard bounded-dimension arrangement bound.
It also checks that each filtered residual-kernel equation is exactly the
divisible short Hankel equation obtained by multiplying back the anchor
locator.
For residual collisions, it audits the one-root version of the resulting
root-slice charge: shared residual roots must be roots of a nonzero lower
degree direction in this divisible short kernel.
Equivalently, the bad-root test is checked as a full-column-rank test for the
absorbed-anchor filtered Hankel matrix.
The resulting absorbed-rank incidence bound is asserted for every enumerated
residual fiber.
It also audits the endpoint-rank test forced by persistent moving kernels for
each produced deficit anchor, and checks that endpoint defects are contained in
the filtered residual-kernel direction space.
When that residual direction space is one-dimensional, it extracts the unique
direction polynomial and checks the resulting root-slice packing bound.
For higher positive residual direction dimension, it audits the direction-MDS
rank-defect packing bound on bad b-subsets.
It also identifies those bad b-subsets with the projective root shadows of the
residual direction space and with absorbed multi-root fixed-divisor rank
defects.
It then checks the resulting projective root-count bound for the bad-subset
ledger, and that every higher bad subset is contained in the one-root bad-slice
ledger.
In the nonpersistent one-root pencil branch, it checks the resulting
field-size-free bad-subset bound.
When full-field probing certifies genuine persistence, it checks that the
persistent branch has an endpoint defect and residual direction dimension at
least two.
Conversely, residual direction dimension at least two forces every available
root to be a one-root bad slice, hence forces the one-root pencil into the
persistent branch for produced anchors in the usual field-size range.
For two-dimensional residual direction spaces, it identifies the bad pairs as
projective evaluation fibers and checks the resulting cross-fiber good-pair
packing bound.
It also computes support-level base/fiber occupancy and checks the resulting
concentration lower bound for good pairs.
It further checks the dominant-fiber escape inequality used by the weighted
good-pair ledger: if L non-base support roots have e roots outside their
largest projective fiber, then the support contains at least L e / 2 good
pairs.
It checks the corresponding quotient certificate: after removing the dominant
base or projective-fiber slice of a support, the residual direction descends
to a quotient kernel whose width is the complement size.
Equivalently, it checks the global root-shadow-height bound: if the largest
base locus or projective fiber has height h, every residual support has the
good-pair lower bound forced by h.
For each fixed collapsed anchor base, it audits the sparse-representation
fiber: below the boundary the mode support is unique, while at the boundary
distinct supports are disjoint and obey the matching bound.
It also checks that absorbing any subset of packet modes into the anchor gives
the predicted smaller sparse packet, with no proper-subset zero collapse.
Consequently it records the number of intrinsic zero-free ordered mode flags
inside these collapsed split-support packets.
Equivalently, it records support-unique boundary packets as those with no
equal-size visible alias.
The full-domain visible endpoint count is then support-unique labels plus one
representative for each complementary root-linear pair.

It also checks the full-top zero-syndrome lemma: if all j+1 complements
U\\{x} inside one (j+1)-top set U are active, then the combined syndrome is
zero.  Thus full top packets belong to the global-codeword/tangent ledger.
Consequently every nonzero top packet has at most j active complements; the
script records the exact active-size profile.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter
from typing import Sequence

from scan_m1_exact_target_v0 import cyclic_subgroup, support_records
from verify_m1_exact_target_hankel_equivalence import (
    hankel_annihilates,
    locator_coeffs,
    support_hankel_records,
)


def is_one_exchange(left: Sequence[int], right: Sequence[int], j: int) -> bool:
    return len(set(left) & set(right)) == j - 1


def hankel_apply(
    syn: Sequence[int],
    locator: Sequence[int],
    row_count: int,
    p: int,
) -> tuple[int, ...]:
    return tuple(
        sum(locator[offset] * syn[row + offset] for offset in range(len(locator))) % p
        for row in range(row_count)
    )


def shift_locator(locator: Sequence[int], shift: int) -> tuple[int, ...]:
    return (0,) * shift + tuple(locator)


def multiply_polynomials_mod(
    left: Sequence[int],
    right: Sequence[int],
    p: int,
) -> tuple[int, ...]:
    product = [0] * (len(left) + len(right) - 1)
    for left_degree, left_coeff in enumerate(left):
        for right_degree, right_coeff in enumerate(right):
            product[left_degree + right_degree] = (
                product[left_degree + right_degree]
                + left_coeff * right_coeff
            ) % p
    return tuple(product)


def divide_by_polynomial_exact_mod(
    numerator: Sequence[int],
    divisor: Sequence[int],
    p: int,
) -> tuple[int, ...]:
    if not divisor or not any(coeff % p for coeff in divisor):
        raise ValueError("zero divisor")
    divisor_degree = len(divisor) - 1
    while divisor_degree > 0 and divisor[divisor_degree] % p == 0:
        divisor_degree -= 1
    divisor_coeffs = [coeff % p for coeff in divisor[: divisor_degree + 1]]
    if len(numerator) < len(divisor_coeffs):
        if any(coeff % p for coeff in numerator):
            raise ValueError("nonzero remainder")
        return (0,)
    remainder = [coeff % p for coeff in numerator]
    quotient = [0] * (len(numerator) - len(divisor_coeffs) + 1)
    inverse_lead = pow(divisor_coeffs[-1], -1, p)
    for offset in range(len(quotient) - 1, -1, -1):
        coeff = remainder[offset + len(divisor_coeffs) - 1] * inverse_lead % p
        quotient[offset] = coeff
        if not coeff:
            continue
        for index, divisor_coeff in enumerate(divisor_coeffs):
            remainder[offset + index] = (
                remainder[offset + index] - coeff * divisor_coeff
            ) % p
    if any(remainder):
        raise ValueError("nonzero remainder")
    return tuple(quotient)


def root_difference_syndrome(
    syn: Sequence[int],
    root: int,
    p: int,
) -> tuple[int, ...]:
    return tuple(
        (syn[index + 1] - root * syn[index]) % p
        for index in range(len(syn) - 1)
    )


def iterated_root_difference_syndrome(
    syn: Sequence[int],
    roots: Sequence[int],
    p: int,
) -> tuple[int, ...]:
    current = tuple(syn)
    for root in roots:
        current = root_difference_syndrome(current, root, p)
    return current


def rank_2_by_2(rows: Sequence[tuple[int, int]], p: int) -> int:
    determinant = (rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]) % p
    if determinant:
        return 2
    if any(value % p for row in rows for value in row):
        return 1
    return 0


def determinant_mod(matrix: Sequence[Sequence[int]], p: int) -> int:
    rows = [list(row) for row in matrix]
    determinant = 1
    for column in range(len(rows)):
        pivot = next(
            (row for row in range(column, len(rows)) if rows[row][column] % p),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            determinant = (-determinant) % p
        pivot_value = rows[column][column] % p
        determinant = determinant * pivot_value % p
        inverse_pivot = pow(pivot_value, -1, p)
        for row in range(column + 1, len(rows)):
            factor = rows[row][column] * inverse_pivot % p
            if not factor:
                continue
            for entry in range(column, len(rows)):
                rows[row][entry] = (
                    rows[row][entry] - factor * rows[column][entry]
                ) % p
    return determinant % p


def matrix_rank_mod(matrix: Sequence[Sequence[int]], p: int) -> int:
    rows = [list(row) for row in matrix if any(value % p for value in row)]
    if not rows:
        return 0
    row_count = len(rows)
    column_count = len(rows[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(rank, row_count)
                if rows[row][column] % p
            ),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse_pivot = pow(rows[rank][column] % p, -1, p)
        for entry in range(column, column_count):
            rows[rank][entry] = rows[rank][entry] * inverse_pivot % p
        for row in range(row_count):
            if row == rank:
                continue
            factor = rows[row][column] % p
            if not factor:
                continue
            for entry in range(column, column_count):
                rows[row][entry] = (
                    rows[row][entry] - factor * rows[rank][entry]
                ) % p
        rank += 1
        if rank == row_count:
            break
    return rank


def right_kernel_basis_mod(
    matrix: Sequence[Sequence[int]],
    p: int,
) -> tuple[tuple[int, ...], ...]:
    column_count = len(matrix[0]) if matrix else 0
    rows = [list(row) for row in matrix if any(value % p for value in row)]
    if not rows:
        return tuple(
            tuple(1 if index == column else 0 for index in range(column_count))
            for column in range(column_count)
        )
    row_count = len(rows)
    rank = 0
    pivot_columns: list[int] = []
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(rank, row_count)
                if rows[row][column] % p
            ),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse_pivot = pow(rows[rank][column] % p, -1, p)
        for entry in range(column, column_count):
            rows[rank][entry] = rows[rank][entry] * inverse_pivot % p
        for row in range(row_count):
            if row == rank:
                continue
            factor = rows[row][column] % p
            if not factor:
                continue
            for entry in range(column, column_count):
                rows[row][entry] = (
                    rows[row][entry] - factor * rows[rank][entry]
                ) % p
        pivot_columns.append(column)
        rank += 1
        if rank == row_count:
            break
    pivot_set = set(pivot_columns)
    basis = []
    for free_column in range(column_count):
        if free_column in pivot_set:
            continue
        vector = [0] * column_count
        vector[free_column] = 1
        for pivot_row, pivot_column in enumerate(pivot_columns):
            vector[pivot_column] = (-rows[pivot_row][free_column]) % p
        basis.append(tuple(vector))
    return tuple(basis)


def polynomial_eval_mod(
    coeffs: Sequence[int],
    value: int,
    p: int,
) -> int:
    result = 0
    for coeff in reversed(coeffs):
        result = (result * value + coeff) % p
    return result


def projective_span_representatives_mod(
    basis: Sequence[Sequence[int]],
    p: int,
) -> tuple[tuple[int, ...], ...]:
    if not basis:
        return ()
    width = len(basis[0])
    representatives: set[tuple[int, ...]] = set()
    for coeffs in itertools.product(range(p), repeat=len(basis)):
        if not any(coeffs):
            continue
        vector = [0] * width
        for coeff, basis_vector in zip(coeffs, basis):
            if not coeff:
                continue
            for index, value in enumerate(basis_vector):
                vector[index] = (vector[index] + coeff * value) % p
        pivot = next((value for value in vector if value % p), None)
        if pivot is None:
            continue
        inverse_pivot = pow(pivot, -1, p)
        representatives.add(
            tuple((value * inverse_pivot) % p for value in vector)
        )
    return tuple(sorted(representatives))


def binomial_or_zero(n: int, k: int) -> int:
    if n < 0 or k < 0 or k > n:
        return 0
    return math.comb(n, k)


def capped_pair_cluster_bound(total: int, cap: int) -> int:
    if total <= 1 or cap <= 1:
        return 0
    full_blocks, remainder = divmod(total, cap)
    return (
        full_blocks * math.comb(cap, 2)
        + math.comb(remainder, 2)
    )


def b2_good_pair_lower_from_slice_height(
    residual_size: int,
    slice_height: int,
) -> int:
    nonbase_lower_count = max(residual_size - slice_height, 0)
    return (
        math.comb(nonbase_lower_count, 2)
        - capped_pair_cluster_bound(
            nonbase_lower_count,
            slice_height,
        )
    )


def hankel_divisor_matrix_mod(
    syn: Sequence[int],
    divisor_locator: Sequence[int],
    row_count: int,
    column_count: int,
    p: int,
) -> tuple[tuple[int, ...], ...]:
    columns = tuple(
        hankel_apply(
            syn,
            shift_locator(divisor_locator, column),
            row_count,
            p,
        )
        for column in range(column_count)
    )
    return tuple(
        tuple(columns[column][row] for column in range(column_count))
        for row in range(row_count)
    )


def solve_square_mod(
    matrix: Sequence[Sequence[int]],
    rhs: Sequence[int],
    p: int,
) -> tuple[int, ...]:
    rows = [list(row) + [rhs[index] % p] for index, row in enumerate(matrix)]
    size = len(rows)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if rows[row][column] % p),
            None,
        )
        if pivot is None:
            raise ValueError("singular matrix")
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
        pivot_value = rows[column][column] % p
        inverse_pivot = pow(pivot_value, -1, p)
        for entry in range(column, size + 1):
            rows[column][entry] = rows[column][entry] * inverse_pivot % p
        for row in range(size):
            if row == column:
                continue
            factor = rows[row][column] % p
            if not factor:
                continue
            for entry in range(column, size + 1):
                rows[row][entry] = (
                    rows[row][entry] - factor * rows[column][entry]
                ) % p
    return tuple(row[-1] % p for row in rows)


def sparse_moment_amplitudes(
    roots: Sequence[int],
    moments: Sequence[int],
    p: int,
) -> tuple[int, ...] | None:
    size = len(roots)
    if len(moments) < size:
        return None
    vandermonde = tuple(
        tuple(pow(root, row, p) for root in roots)
        for row in range(size)
    )
    amplitudes = solve_square_mod(vandermonde, moments[:size], p)
    for row, moment in enumerate(moments):
        if (
            sum(
                amplitude * pow(root, row, p)
                for amplitude, root in zip(amplitudes, roots)
            )
            % p
            != moment % p
        ):
            return None
    return amplitudes


def augmented_consistent(rows: Sequence[tuple[int, int, int]], p: int) -> bool:
    for left, right in itertools.combinations(rows, 2):
        if (
            (left[0] * right[1] - left[1] * right[0]) % p
            or (left[0] * right[2] - left[2] * right[0]) % p
            or (left[1] * right[2] - left[2] * right[1]) % p
        ):
            return False
    return True


def classify_core_plane(
    syn: Sequence[int],
    core_locator: Sequence[int],
    p: int,
) -> tuple[str, dict[str, int]]:
    """Classify active two-root extensions over a fixed (j-2)-core."""
    constant = hankel_apply(syn, shift_locator(core_locator, 2), 2, p)
    sigma_vector = hankel_apply(syn, shift_locator(core_locator, 1), 2, p)
    pi_vector = hankel_apply(syn, core_locator, 2, p)
    rows = [
        ((-sigma_vector[row]) % p, pi_vector[row] % p, (-constant[row]) % p)
        for row in range(2)
    ]
    coefficient_rows = [(row[0], row[1]) for row in rows]
    coefficient_rank = rank_2_by_2(coefficient_rows, p)
    if coefficient_rank == 2:
        return ("point", {})
    if coefficient_rank == 0:
        if any(row[2] for row in rows):
            return ("empty_inconsistent", {})
        return ("full_plane", {})
    if not augmented_consistent(rows, p):
        return ("empty_inconsistent", {})

    alpha, beta, gamma = next(row for row in rows if row[0] or row[1])
    if beta == 0:
        return ("fixed_sum_line", {"sum": gamma * pow(alpha, -1, p) % p})

    slope = (-alpha) * pow(beta, -1, p) % p
    intercept = gamma * pow(beta, -1, p) % p
    mu = (slope * slope + intercept) % p
    if mu == 0:
        return ("fixed_root_line", {"root": slope})
    return ("product_mobius_line", {"center": slope, "mu": mu})


def classify_triangle(
    complements: Sequence[Sequence[int]],
    j: int,
) -> tuple[str, tuple[int, ...]]:
    sets = [set(complement) for complement in complements]
    common = set.intersection(*sets)
    union = set.union(*sets)
    if len(common) == j - 1:
        return ("star", tuple(sorted(common)))
    if len(union) == j + 1:
        return ("top", tuple(sorted(union)))
    raise AssertionError(
        {
            "kind": "unclassified-one-exchange-triangle",
            "j": j,
            "complements": [list(complement) for complement in complements],
            "common": sorted(common),
            "union": sorted(union),
        }
    )


def analyze_case(
    p: int,
    k: int,
    max_syndromes: int,
    max_examples: int,
) -> dict[str, object]:
    n = p - 1
    t = 2
    a = k + t
    j = n - a
    r = n - k
    if not (0 < k < a <= n):
        raise ValueError("case must satisfy 0 < k and k+2 <= p-1")
    if j < 1:
        raise ValueError("one-exchange packets require j >= 1")
    syndrome_count = p**r
    if syndrome_count > max_syndromes:
        raise ValueError(
            f"would enumerate {syndrome_count} syndromes; "
            f"raise --max-syndromes to run this exact case"
        )

    domain = cyclic_subgroup(p, n)
    support_hankels = support_hankel_records(domain, support_records(n, a), p)
    complements = [tuple(record["complement_indices"]) for record in support_hankels]
    locators = [tuple(record["locator"]) for record in support_hankels]
    complement_index = {
        complement: index for index, complement in enumerate(complements)
    }
    locator_cache: dict[tuple[int, ...], tuple[int, ...]] = {}
    domain_index_by_value = {value: index for index, value in enumerate(domain)}

    def cached_locator(core: tuple[int, ...]) -> tuple[int, ...]:
        if core not in locator_cache:
            locator_cache[core] = locator_coeffs(domain, core, p)
        return locator_cache[core]

    one_exchange_neighbors: list[list[int]] = [[] for _ in complements]
    for left, right in itertools.combinations(range(len(complements)), 2):
        if not is_one_exchange(complements[left], complements[right], j):
            continue
        one_exchange_neighbors[left].append(right)
        one_exchange_neighbors[right].append(left)

    core_planes: list[dict[str, object]] = []
    if j >= 2:
        for core in itertools.combinations(range(n), j - 2):
            core_set = set(core)
            pair_members: list[int] = []
            added_pairs: list[tuple[int, int]] = []
            for index, complement in enumerate(complements):
                complement_set = set(complement)
                if not core_set.issubset(complement_set):
                    continue
                added = tuple(sorted(complement_set - core_set))
                if len(added) != 2:
                    continue
                pair_members.append(index)
                added_pairs.append(added)
            core_planes.append(
                {
                    "core": core,
                    "core_set": core_set,
                    "core_locator": cached_locator(core),
                    "pair_members": pair_members,
                    "added_pairs": added_pairs,
                }
            )

    active_histogram: Counter[int] = Counter()
    edge_histogram: Counter[int] = Counter()
    triangle_histogram: Counter[int] = Counter()
    core_plane_histogram: Counter[str] = Counter()
    nonzero_core_plane_histogram: Counter[str] = Counter()
    nonzero_core_plane_active_pair_histogram: Counter[int] = Counter()
    corner_histogram: Counter[str] = Counter()
    nonzero_corner_histogram: Counter[str] = Counter()
    component_histogram: Counter[str] = Counter()
    nonzero_component_histogram: Counter[str] = Counter()
    component_size_histogram: Counter[str] = Counter()
    nonzero_component_size_histogram: Counter[str] = Counter()
    nonisolated_ledger_slack_histogram: Counter[int] = Counter()
    nonstar_component_ledger_slack_histogram: Counter[int] = Counter()
    isolated_vertex_histogram: Counter[int] = Counter()
    isolated_boundary_zero_histogram: Counter[int] = Counter()
    isolated_marked_boundary_slack_histogram: Counter[int] = Counter()
    full_support_ledger_slack_histogram: Counter[int] = Counter()
    first_boundary_zero_core_histogram: Counter[int] = Counter()
    first_boundary_incidence_defect_histogram: Counter[int] = Counter()
    fixed_root_decomposition_defect_histogram: Counter[int] = Counter()
    fixed_root_difference_defect_histogram: Counter[int] = Counter()
    root_marked_single_row_defect_histogram: Counter[int] = Counter()
    root_marked_edge_core_slack_histogram: Counter[int] = Counter()
    root_marked_isolated_histogram: Counter[int] = Counter()
    residual_boundary_slack_histogram: Counter[int] = Counter()
    iterated_difference_checks = 0
    iterated_difference_defect_histogram: Counter[int] = Counter()
    iterated_boundary_identity_checks = 0
    fixed_root_filtration_pair_checks = 0
    filtration_path_checks = 0
    filtration_zero_stop_paths = 0
    filtration_terminal_paths = 0
    filtration_nonzero_scalar_steps = 0
    terminal_bottom_support_checks = 0
    terminal_support_bound_capacity = 0
    terminal_tree_recursion_checks = 0
    terminal_tree_branch_vertices = 0
    terminal_tree_branch_pair_checks = 0
    terminal_tree_productive_branch_pairs = 0
    terminal_tree_mode_packet_checks = 0
    terminal_tree_productive_mode_packets = 0
    terminal_tree_mode_anchor_reconstruction_checks = 0
    terminal_tree_productive_mode_anchor_reconstruction_checks = 0
    terminal_tree_visible_packet_labels = 0
    terminal_tree_productive_visible_packet_labels = 0
    terminal_tree_visible_packet_repeated_labels = 0
    terminal_tree_productive_visible_packet_repeated_labels = 0
    terminal_tree_visible_packet_excess_productions = 0
    terminal_tree_productive_visible_packet_excess_productions = 0
    terminal_tree_visible_packet_max_fiber_size = 0
    terminal_tree_productive_visible_packet_max_fiber_size = 0
    terminal_tree_anchor_base_image_checks = 0
    terminal_tree_productive_anchor_base_image_checks = 0
    terminal_tree_anchor_base_kernel_checks = 0
    terminal_tree_productive_anchor_base_kernel_checks = 0
    terminal_tree_anchor_base_one_exchange_core_checks = 0
    terminal_tree_productive_anchor_base_one_exchange_core_checks = 0
    terminal_tree_anchor_base_one_exchange_kernel_hits = 0
    terminal_tree_productive_anchor_base_one_exchange_kernel_hits = 0
    terminal_tree_anchor_split_support_checks = 0
    terminal_tree_productive_anchor_split_support_checks = 0
    terminal_tree_anchor_split_boundary_checks = 0
    terminal_tree_productive_anchor_split_boundary_checks = 0
    terminal_tree_anchor_split_roundtrip_checks = 0
    terminal_tree_productive_anchor_split_roundtrip_checks = 0
    terminal_tree_anchor_split_absorption_checks = 0
    terminal_tree_productive_anchor_split_absorption_checks = 0
    terminal_tree_anchor_split_proper_absorption_checks = 0
    terminal_tree_productive_anchor_split_proper_absorption_checks = 0
    terminal_tree_anchor_split_ordered_mode_flags = 0
    terminal_tree_productive_anchor_split_ordered_mode_flags = 0
    terminal_tree_total_split_support_fiber_checks = 0
    terminal_tree_productive_total_split_support_fiber_checks = 0
    terminal_tree_total_split_support_fiber_labels = 0
    terminal_tree_productive_total_split_support_fiber_labels = 0
    terminal_tree_total_split_support_fiber_max_size = 0
    terminal_tree_productive_total_split_support_fiber_max_size = 0
    terminal_tree_total_split_support_factorization_checks = 0
    terminal_tree_productive_total_split_support_factorization_checks = 0
    terminal_tree_total_split_support_max_marked_roots = 0
    terminal_tree_productive_total_split_support_max_marked_roots = 0
    terminal_tree_marked_exit_cube_support_checks = 0
    terminal_tree_productive_marked_exit_cube_support_checks = 0
    terminal_tree_marked_exit_cube_face_checks = 0
    terminal_tree_productive_marked_exit_cube_face_checks = 0
    terminal_tree_marked_exit_cube_ordered_flags = 0
    terminal_tree_productive_marked_exit_cube_ordered_flags = 0
    terminal_tree_marked_exit_cube_max_marked_roots = 0
    terminal_tree_productive_marked_exit_cube_max_marked_roots = 0
    terminal_tree_marked_core_fiber_checks = 0
    terminal_tree_productive_marked_core_fiber_checks = 0
    terminal_tree_marked_core_fiber_labels = 0
    terminal_tree_productive_marked_core_fiber_labels = 0
    terminal_tree_marked_core_fiber_max_size = 0
    terminal_tree_productive_marked_core_fiber_max_size = 0
    terminal_tree_marked_core_nonempty_boundary_checks = 0
    terminal_tree_productive_marked_core_nonempty_boundary_checks = 0
    terminal_tree_marked_core_nonempty_boundary_max_size = 0
    terminal_tree_productive_marked_core_nonempty_boundary_max_size = 0
    terminal_tree_empty_core_boundary_fiber_checks = 0
    terminal_tree_productive_empty_core_boundary_fiber_checks = 0
    terminal_tree_empty_core_boundary_fiber_labels = 0
    terminal_tree_productive_empty_core_boundary_fiber_labels = 0
    terminal_tree_empty_core_boundary_fiber_max_size = 0
    terminal_tree_productive_empty_core_boundary_fiber_max_size = 0
    terminal_tree_empty_core_boundary_root_linear_checks = 0
    terminal_tree_productive_empty_core_boundary_root_linear_checks = 0
    terminal_tree_empty_core_boundary_root_linear_hits = 0
    terminal_tree_productive_empty_core_boundary_root_linear_hits = 0
    terminal_tree_empty_core_boundary_complement_pair_checks = 0
    terminal_tree_productive_empty_core_boundary_complement_pair_checks = 0
    terminal_tree_moment_complete_core_checks = 0
    terminal_tree_productive_moment_complete_core_checks = 0
    terminal_tree_moment_complete_core_max_fiber_size = 0
    terminal_tree_productive_moment_complete_core_max_fiber_size = 0
    terminal_tree_deficit_packing_core_checks = 0
    terminal_tree_productive_deficit_packing_core_checks = 0
    terminal_tree_deficit_packing_core_max_deficit = 0
    terminal_tree_productive_deficit_packing_core_max_deficit = 0
    terminal_tree_deficit_packing_core_max_fiber_size = 0
    terminal_tree_productive_deficit_packing_core_max_fiber_size = 0
    terminal_tree_deficit_anchor_label_checks = 0
    terminal_tree_productive_deficit_anchor_label_checks = 0
    terminal_tree_deficit_anchor_max_labels_per_fiber = 0
    terminal_tree_productive_deficit_anchor_max_labels_per_fiber = 0
    terminal_tree_deficit_anchor_kernel_checks = 0
    terminal_tree_productive_deficit_anchor_kernel_checks = 0
    terminal_tree_deficit_anchor_max_residual_size = 0
    terminal_tree_productive_deficit_anchor_max_residual_size = 0
    terminal_tree_deficit_anchor_residual_fiber_checks = 0
    terminal_tree_productive_deficit_anchor_residual_fiber_checks = 0
    terminal_tree_deficit_anchor_residual_fiber_labels = 0
    terminal_tree_productive_deficit_anchor_residual_fiber_labels = 0
    terminal_tree_deficit_anchor_residual_fiber_max_size = 0
    terminal_tree_productive_deficit_anchor_residual_fiber_max_size = 0
    terminal_tree_deficit_anchor_residual_fiber_max_direction = 0
    terminal_tree_productive_deficit_anchor_residual_fiber_max_direction = 0
    terminal_tree_deficit_anchor_line_kernel_checks = 0
    terminal_tree_productive_deficit_anchor_line_kernel_checks = 0
    terminal_tree_deficit_anchor_line_kernel_max_direction_roots = 0
    terminal_tree_productive_deficit_anchor_line_kernel_max_direction_roots = 0
    terminal_tree_deficit_anchor_line_kernel_max_sharp_bound = 0
    terminal_tree_productive_deficit_anchor_line_kernel_max_sharp_bound = 0
    terminal_tree_deficit_anchor_direction_mds_checks = 0
    terminal_tree_productive_deficit_anchor_direction_mds_checks = 0
    terminal_tree_deficit_anchor_direction_mds_bad_subsets = 0
    terminal_tree_productive_deficit_anchor_direction_mds_bad_subsets = 0
    terminal_tree_deficit_anchor_direction_mds_max_bad_subsets = 0
    terminal_tree_productive_deficit_anchor_direction_mds_max_bad_subsets = 0
    terminal_tree_deficit_anchor_direction_mds_max_bound = 0
    terminal_tree_productive_deficit_anchor_direction_mds_max_bound = 0
    terminal_tree_deficit_anchor_root_slice_checks = 0
    terminal_tree_productive_deficit_anchor_root_slice_checks = 0
    terminal_tree_deficit_anchor_root_slice_labels = 0
    terminal_tree_productive_deficit_anchor_root_slice_labels = 0
    terminal_tree_deficit_anchor_root_slice_bad_labels = 0
    terminal_tree_productive_deficit_anchor_root_slice_bad_labels = 0
    terminal_tree_deficit_anchor_root_slice_max_bad_per_anchor = 0
    terminal_tree_productive_deficit_anchor_root_slice_max_bad_per_anchor = 0
    terminal_tree_deficit_anchor_endpoint_rank_checks = 0
    terminal_tree_productive_deficit_anchor_endpoint_rank_checks = 0
    terminal_tree_deficit_anchor_endpoint_rank_defects = 0
    terminal_tree_productive_deficit_anchor_endpoint_rank_defects = 0
    terminal_tree_deficit_anchor_endpoint_rank_max_defect = 0
    terminal_tree_productive_deficit_anchor_endpoint_rank_max_defect = 0
    terminal_tree_core_packet_checks = 0
    terminal_tree_productive_core_packet_checks = 0
    terminal_tree_core_simple_pole_lift_checks = 0
    terminal_tree_productive_core_simple_pole_lift_checks = 0
    terminal_tree_unmarked_zero_cube_support_checks = 0
    terminal_tree_productive_unmarked_zero_cube_support_checks = 0
    terminal_tree_unmarked_zero_cube_face_checks = 0
    terminal_tree_productive_unmarked_zero_cube_face_checks = 0
    terminal_tree_unmarked_zero_cube_max_unmarked_roots = 0
    terminal_tree_productive_unmarked_zero_cube_max_unmarked_roots = 0
    terminal_tree_mixed_marked_zero_cube_support_checks = 0
    terminal_tree_productive_mixed_marked_zero_cube_support_checks = 0
    terminal_tree_mixed_marked_zero_cube_face_checks = 0
    terminal_tree_productive_mixed_marked_zero_cube_face_checks = 0
    terminal_tree_mixed_marked_zero_cube_max_deleted_unmarked_roots = 0
    terminal_tree_productive_mixed_marked_zero_cube_max_deleted_unmarked_roots = 0
    terminal_tree_unmarked_shift_marking_support_checks = 0
    terminal_tree_productive_unmarked_shift_marking_support_checks = 0
    terminal_tree_unmarked_shift_marking_root_checks = 0
    terminal_tree_productive_unmarked_shift_marking_root_checks = 0
    terminal_tree_unmarked_shift_marking_max_deleted_roots = 0
    terminal_tree_productive_unmarked_shift_marking_max_deleted_roots = 0
    terminal_tree_anchor_fiber_checks = 0
    terminal_tree_productive_anchor_fiber_checks = 0
    terminal_tree_anchor_fiber_labels = 0
    terminal_tree_productive_anchor_fiber_labels = 0
    terminal_tree_anchor_fiber_max_size = 0
    terminal_tree_productive_anchor_fiber_max_size = 0
    terminal_tree_mode_rank_checks = 0
    terminal_tree_productive_mode_rank_checks = 0
    terminal_tree_mode_peeling_checks = 0
    terminal_tree_productive_mode_peeling_checks = 0
    terminal_tree_mode_annihilator_checks = 0
    terminal_tree_productive_mode_annihilator_checks = 0
    terminal_tree_boundary_alias_checks = 0
    terminal_tree_productive_boundary_alias_checks = 0
    terminal_tree_boundary_aliases = 0
    terminal_tree_productive_boundary_aliases = 0
    terminal_tree_boundary_scalar_fit_candidate_checks = 0
    terminal_tree_productive_boundary_scalar_fit_candidate_checks = 0
    terminal_tree_boundary_scalar_fits = 0
    terminal_tree_productive_boundary_scalar_fits = 0
    terminal_tree_boundary_root_linear_checks = 0
    terminal_tree_productive_boundary_root_linear_checks = 0
    terminal_tree_boundary_root_linear_hits = 0
    terminal_tree_productive_boundary_root_linear_hits = 0
    terminal_tree_boundary_root_linear_by_support: Counter[tuple[int, ...]] = (
        Counter()
    )
    terminal_tree_boundary_support_unique = 0
    terminal_tree_productive_boundary_support_unique = 0
    terminal_tree_boundary_max_fiber_size = 0
    terminal_tree_productive_boundary_max_fiber_size = 0
    terminal_tree_mode_sizes_seen: set[int] = set()
    terminal_tree_boundary_mode_sizes_seen: set[int] = set()
    terminal_tree_multiflag_cores = 0
    iterated_boundary_defect_histogram: Counter[int] = Counter()
    fixed_root_filtration_defect_histogram: Counter[int] = Counter()
    filtration_path_defect_histogram: Counter[int] = Counter()
    filtration_path_partition_defect_histogram: Counter[int] = Counter()
    filtration_zero_stop_depth_histogram: Counter[int] = Counter()
    terminal_support_bound_slack_histogram: Counter[int] = Counter()
    terminal_tree_recursion_defect_histogram: Counter[int] = Counter()
    terminal_tree_branch_vertex_histogram: Counter[int] = Counter()
    terminal_tree_branch_pair_histogram: Counter[int] = Counter()
    terminal_tree_productive_branch_pair_histogram: Counter[int] = Counter()
    terminal_tree_mode_packet_histogram: Counter[int] = Counter()
    terminal_tree_productive_mode_packet_histogram: Counter[int] = Counter()
    terminal_tree_visible_packet_fiber_size_histogram: Counter[int] = Counter()
    terminal_tree_productive_visible_packet_fiber_size_histogram: Counter[int] = (
        Counter()
    )
    terminal_tree_mode_size_histogram: Counter[int] = Counter()
    terminal_tree_productive_mode_size_histogram: Counter[int] = Counter()
    terminal_tree_mode_rank_histogram: Counter[int] = Counter()
    terminal_tree_productive_mode_rank_histogram: Counter[int] = Counter()
    terminal_tree_mode_rank_size_histogram: Counter[int] = Counter()
    terminal_tree_mode_peeling_histogram: Counter[int] = Counter()
    terminal_tree_productive_mode_peeling_histogram: Counter[int] = Counter()
    terminal_tree_mode_peeling_subset_size_histogram: Counter[int] = Counter()
    terminal_tree_mode_annihilator_histogram: Counter[int] = Counter()
    terminal_tree_productive_mode_annihilator_histogram: Counter[int] = Counter()
    terminal_tree_mode_annihilator_size_histogram: Counter[int] = Counter()
    terminal_tree_boundary_alias_histogram: Counter[int] = Counter()
    terminal_tree_productive_boundary_alias_histogram: Counter[int] = Counter()
    terminal_tree_boundary_scalar_fit_histogram: Counter[int] = Counter()
    terminal_tree_productive_boundary_scalar_fit_histogram: Counter[int] = Counter()
    terminal_tree_boundary_root_linear_histogram: Counter[int] = Counter()
    terminal_tree_productive_boundary_root_linear_histogram: Counter[int] = Counter()
    terminal_tree_boundary_fiber_size_histogram: Counter[int] = Counter()
    terminal_tree_productive_boundary_fiber_size_histogram: Counter[int] = Counter()
    terminal_tree_multiflag_core_histogram: Counter[int] = Counter()
    max_active = 0
    max_edges = 0
    max_triangles = 0
    max_nonzero_core_plane_active_pairs = 0
    max_nonzero_star_corners_per_syndrome = 0
    max_nonzero_lower_core_corners_per_syndrome = 0
    max_nonzero_star_component_size = 0
    max_nonzero_lower_core_component_size = 0
    max_nonzero_edge_core_count = 0
    max_nonzero_lower_core_witness_count = 0
    max_nonzero_nonisolated_ledger_slack = 0
    max_nonzero_nonstar_component_ledger_slack = 0
    max_nonzero_isolated_vertices = 0
    max_nonzero_root_marked_boundary_count = 0
    max_nonzero_isolated_marked_boundary_slack = 0
    max_nonzero_full_support_ledger_slack = 0
    max_nonzero_first_boundary_zero_core_count = 0
    max_nonzero_fixed_root_active_count = 0
    max_nonzero_fixed_root_difference_kernel_count = 0
    max_nonzero_root_marked_per_root = 0
    max_nonzero_root_marked_single_row_count = 0
    max_nonzero_root_marked_slice_edges = 0
    max_nonzero_root_marked_edge_core_count = 0
    max_nonzero_root_marked_edge_core_slack = 0
    max_nonzero_root_marked_isolated_count = 0
    max_nonzero_residual_boundary_count = 0
    max_nonzero_residual_boundary_slack = 0
    max_iterated_difference_chain_length = 0
    max_iterated_boundary_chain_length = 0
    max_nonzero_iterated_boundary_active_cores = 0
    max_nonzero_iterated_boundary_zero_cores = 0
    max_nonzero_iterated_boundary_marked = 0
    max_nonzero_fixed_root_filtration_pairs = 0
    max_nonzero_filtration_paths = 0
    max_nonzero_zero_stop_filtration_paths = 0
    max_nonzero_terminal_filtration_paths = 0
    max_nonzero_filtration_nonzero_scalar_steps = 0
    max_nonzero_terminal_bottom_supports = 0
    max_nonzero_terminal_support_bound_slack = 0
    max_nonzero_terminal_tree_count = 0
    max_nonzero_terminal_tree_branch_vertices = 0
    max_nonzero_terminal_tree_branch_pairs = 0
    max_nonzero_terminal_tree_productive_branch_pairs = 0
    max_nonzero_terminal_tree_mode_packets = 0
    max_nonzero_terminal_tree_productive_mode_packets = 0
    max_nonzero_terminal_tree_visible_packet_fiber_size = 0
    max_nonzero_terminal_tree_productive_visible_packet_fiber_size = 0
    max_nonzero_terminal_tree_mode_size = 0
    max_nonzero_terminal_tree_mode_rank_checks = 0
    max_nonzero_terminal_tree_mode_rank_size = 0
    max_nonzero_terminal_tree_mode_peeling_checks = 0
    max_nonzero_terminal_tree_mode_annihilator_checks = 0
    max_nonzero_terminal_tree_multiflag_cores = 0
    one_exchange_edges = 0
    star_triangles = 0
    top_triangles = 0
    nonzero_top_triangles = 0
    full_top_cliques = 0
    nonzero_full_top_cliques = 0
    max_nonzero_top_active_members = 0
    nonzero_top_active_size_histogram: Counter[int] = Counter()
    star_examples: list[dict[str, object]] = []
    top_examples: list[dict[str, object]] = []
    full_top_examples: list[dict[str, object]] = []

    for syn in itertools.product(range(p), repeat=r):
        case_filtration_path_defect = 0
        case_filtration_paths = 0
        case_zero_stop_filtration_paths = 0
        case_terminal_filtration_paths = 0
        case_filtration_nonzero_scalar_steps = 0

        def audit_filtration_paths(
            fixed_roots: tuple[int, ...],
            active_cores: set[tuple[int, ...]],
        ) -> None:
            nonlocal case_filtration_path_defect
            nonlocal case_filtration_paths
            nonlocal case_zero_stop_filtration_paths
            nonlocal case_terminal_filtration_paths
            nonlocal case_filtration_nonzero_scalar_steps
            nonlocal filtration_path_checks
            nonlocal filtration_zero_stop_paths
            nonlocal filtration_terminal_paths
            nonlocal filtration_nonzero_scalar_steps
            nonlocal terminal_bottom_support_checks
            nonlocal terminal_support_bound_capacity
            nonlocal terminal_tree_recursion_checks
            nonlocal terminal_tree_branch_vertices
            nonlocal terminal_tree_branch_pair_checks
            nonlocal terminal_tree_productive_branch_pairs
            nonlocal terminal_tree_mode_packet_checks
            nonlocal terminal_tree_productive_mode_packets
            nonlocal terminal_tree_mode_anchor_reconstruction_checks
            nonlocal terminal_tree_productive_mode_anchor_reconstruction_checks
            nonlocal terminal_tree_visible_packet_labels
            nonlocal terminal_tree_productive_visible_packet_labels
            nonlocal terminal_tree_visible_packet_repeated_labels
            nonlocal terminal_tree_productive_visible_packet_repeated_labels
            nonlocal terminal_tree_visible_packet_excess_productions
            nonlocal terminal_tree_productive_visible_packet_excess_productions
            nonlocal terminal_tree_visible_packet_max_fiber_size
            nonlocal terminal_tree_productive_visible_packet_max_fiber_size
            nonlocal terminal_tree_anchor_base_image_checks
            nonlocal terminal_tree_productive_anchor_base_image_checks
            nonlocal terminal_tree_anchor_base_kernel_checks
            nonlocal terminal_tree_productive_anchor_base_kernel_checks
            nonlocal terminal_tree_anchor_base_one_exchange_core_checks
            nonlocal terminal_tree_productive_anchor_base_one_exchange_core_checks
            nonlocal terminal_tree_anchor_base_one_exchange_kernel_hits
            nonlocal terminal_tree_productive_anchor_base_one_exchange_kernel_hits
            nonlocal terminal_tree_anchor_split_support_checks
            nonlocal terminal_tree_productive_anchor_split_support_checks
            nonlocal terminal_tree_anchor_split_boundary_checks
            nonlocal terminal_tree_productive_anchor_split_boundary_checks
            nonlocal terminal_tree_anchor_split_roundtrip_checks
            nonlocal terminal_tree_productive_anchor_split_roundtrip_checks
            nonlocal terminal_tree_anchor_split_absorption_checks
            nonlocal terminal_tree_productive_anchor_split_absorption_checks
            nonlocal terminal_tree_anchor_split_proper_absorption_checks
            nonlocal terminal_tree_productive_anchor_split_proper_absorption_checks
            nonlocal terminal_tree_anchor_split_ordered_mode_flags
            nonlocal terminal_tree_productive_anchor_split_ordered_mode_flags
            nonlocal terminal_tree_total_split_support_fiber_checks
            nonlocal terminal_tree_productive_total_split_support_fiber_checks
            nonlocal terminal_tree_total_split_support_fiber_labels
            nonlocal terminal_tree_productive_total_split_support_fiber_labels
            nonlocal terminal_tree_total_split_support_fiber_max_size
            nonlocal terminal_tree_productive_total_split_support_fiber_max_size
            nonlocal terminal_tree_total_split_support_factorization_checks
            nonlocal terminal_tree_productive_total_split_support_factorization_checks
            nonlocal terminal_tree_total_split_support_max_marked_roots
            nonlocal terminal_tree_productive_total_split_support_max_marked_roots
            nonlocal terminal_tree_marked_exit_cube_support_checks
            nonlocal terminal_tree_productive_marked_exit_cube_support_checks
            nonlocal terminal_tree_marked_exit_cube_face_checks
            nonlocal terminal_tree_productive_marked_exit_cube_face_checks
            nonlocal terminal_tree_marked_exit_cube_ordered_flags
            nonlocal terminal_tree_productive_marked_exit_cube_ordered_flags
            nonlocal terminal_tree_marked_exit_cube_max_marked_roots
            nonlocal terminal_tree_productive_marked_exit_cube_max_marked_roots
            nonlocal terminal_tree_marked_core_fiber_checks
            nonlocal terminal_tree_productive_marked_core_fiber_checks
            nonlocal terminal_tree_marked_core_fiber_labels
            nonlocal terminal_tree_productive_marked_core_fiber_labels
            nonlocal terminal_tree_marked_core_fiber_max_size
            nonlocal terminal_tree_productive_marked_core_fiber_max_size
            nonlocal terminal_tree_marked_core_nonempty_boundary_checks
            nonlocal terminal_tree_productive_marked_core_nonempty_boundary_checks
            nonlocal terminal_tree_marked_core_nonempty_boundary_max_size
            nonlocal terminal_tree_productive_marked_core_nonempty_boundary_max_size
            nonlocal terminal_tree_empty_core_boundary_fiber_checks
            nonlocal terminal_tree_productive_empty_core_boundary_fiber_checks
            nonlocal terminal_tree_empty_core_boundary_fiber_labels
            nonlocal terminal_tree_productive_empty_core_boundary_fiber_labels
            nonlocal terminal_tree_empty_core_boundary_fiber_max_size
            nonlocal terminal_tree_productive_empty_core_boundary_fiber_max_size
            nonlocal terminal_tree_empty_core_boundary_root_linear_checks
            nonlocal terminal_tree_productive_empty_core_boundary_root_linear_checks
            nonlocal terminal_tree_empty_core_boundary_root_linear_hits
            nonlocal terminal_tree_productive_empty_core_boundary_root_linear_hits
            nonlocal terminal_tree_empty_core_boundary_complement_pair_checks
            nonlocal terminal_tree_productive_empty_core_boundary_complement_pair_checks
            nonlocal terminal_tree_moment_complete_core_checks
            nonlocal terminal_tree_productive_moment_complete_core_checks
            nonlocal terminal_tree_moment_complete_core_max_fiber_size
            nonlocal terminal_tree_productive_moment_complete_core_max_fiber_size
            nonlocal terminal_tree_deficit_packing_core_checks
            nonlocal terminal_tree_productive_deficit_packing_core_checks
            nonlocal terminal_tree_deficit_packing_core_max_deficit
            nonlocal terminal_tree_productive_deficit_packing_core_max_deficit
            nonlocal terminal_tree_deficit_packing_core_max_fiber_size
            nonlocal terminal_tree_productive_deficit_packing_core_max_fiber_size
            nonlocal terminal_tree_deficit_anchor_label_checks
            nonlocal terminal_tree_productive_deficit_anchor_label_checks
            nonlocal terminal_tree_deficit_anchor_max_labels_per_fiber
            nonlocal terminal_tree_productive_deficit_anchor_max_labels_per_fiber
            nonlocal terminal_tree_deficit_anchor_kernel_checks
            nonlocal terminal_tree_productive_deficit_anchor_kernel_checks
            nonlocal terminal_tree_deficit_anchor_max_residual_size
            nonlocal terminal_tree_productive_deficit_anchor_max_residual_size
            nonlocal terminal_tree_deficit_anchor_residual_fiber_checks
            nonlocal terminal_tree_productive_deficit_anchor_residual_fiber_checks
            nonlocal terminal_tree_deficit_anchor_residual_fiber_labels
            nonlocal terminal_tree_productive_deficit_anchor_residual_fiber_labels
            nonlocal terminal_tree_deficit_anchor_residual_fiber_max_size
            nonlocal terminal_tree_productive_deficit_anchor_residual_fiber_max_size
            nonlocal terminal_tree_deficit_anchor_residual_fiber_max_direction
            nonlocal terminal_tree_productive_deficit_anchor_residual_fiber_max_direction
            nonlocal terminal_tree_deficit_anchor_line_kernel_checks
            nonlocal terminal_tree_productive_deficit_anchor_line_kernel_checks
            nonlocal terminal_tree_deficit_anchor_line_kernel_max_direction_roots
            nonlocal terminal_tree_productive_deficit_anchor_line_kernel_max_direction_roots
            nonlocal terminal_tree_deficit_anchor_line_kernel_max_sharp_bound
            nonlocal terminal_tree_productive_deficit_anchor_line_kernel_max_sharp_bound
            nonlocal terminal_tree_deficit_anchor_direction_mds_checks
            nonlocal terminal_tree_productive_deficit_anchor_direction_mds_checks
            nonlocal terminal_tree_deficit_anchor_direction_mds_bad_subsets
            nonlocal terminal_tree_productive_deficit_anchor_direction_mds_bad_subsets
            nonlocal terminal_tree_deficit_anchor_direction_mds_max_bad_subsets
            nonlocal terminal_tree_productive_deficit_anchor_direction_mds_max_bad_subsets
            nonlocal terminal_tree_deficit_anchor_direction_mds_max_bound
            nonlocal terminal_tree_productive_deficit_anchor_direction_mds_max_bound
            nonlocal terminal_tree_deficit_anchor_root_slice_checks
            nonlocal terminal_tree_productive_deficit_anchor_root_slice_checks
            nonlocal terminal_tree_deficit_anchor_root_slice_labels
            nonlocal terminal_tree_productive_deficit_anchor_root_slice_labels
            nonlocal terminal_tree_deficit_anchor_root_slice_bad_labels
            nonlocal terminal_tree_productive_deficit_anchor_root_slice_bad_labels
            nonlocal terminal_tree_deficit_anchor_root_slice_max_bad_per_anchor
            nonlocal terminal_tree_productive_deficit_anchor_root_slice_max_bad_per_anchor
            nonlocal terminal_tree_deficit_anchor_endpoint_rank_checks
            nonlocal terminal_tree_productive_deficit_anchor_endpoint_rank_checks
            nonlocal terminal_tree_deficit_anchor_endpoint_rank_defects
            nonlocal terminal_tree_productive_deficit_anchor_endpoint_rank_defects
            nonlocal terminal_tree_deficit_anchor_endpoint_rank_max_defect
            nonlocal terminal_tree_productive_deficit_anchor_endpoint_rank_max_defect
            nonlocal terminal_tree_core_packet_checks
            nonlocal terminal_tree_productive_core_packet_checks
            nonlocal terminal_tree_core_simple_pole_lift_checks
            nonlocal terminal_tree_productive_core_simple_pole_lift_checks
            nonlocal terminal_tree_unmarked_zero_cube_support_checks
            nonlocal terminal_tree_productive_unmarked_zero_cube_support_checks
            nonlocal terminal_tree_unmarked_zero_cube_face_checks
            nonlocal terminal_tree_productive_unmarked_zero_cube_face_checks
            nonlocal terminal_tree_unmarked_zero_cube_max_unmarked_roots
            nonlocal terminal_tree_productive_unmarked_zero_cube_max_unmarked_roots
            nonlocal terminal_tree_mixed_marked_zero_cube_support_checks
            nonlocal terminal_tree_productive_mixed_marked_zero_cube_support_checks
            nonlocal terminal_tree_mixed_marked_zero_cube_face_checks
            nonlocal terminal_tree_productive_mixed_marked_zero_cube_face_checks
            nonlocal terminal_tree_mixed_marked_zero_cube_max_deleted_unmarked_roots
            nonlocal terminal_tree_productive_mixed_marked_zero_cube_max_deleted_unmarked_roots
            nonlocal terminal_tree_unmarked_shift_marking_support_checks
            nonlocal terminal_tree_productive_unmarked_shift_marking_support_checks
            nonlocal terminal_tree_unmarked_shift_marking_root_checks
            nonlocal terminal_tree_productive_unmarked_shift_marking_root_checks
            nonlocal terminal_tree_unmarked_shift_marking_max_deleted_roots
            nonlocal terminal_tree_productive_unmarked_shift_marking_max_deleted_roots
            nonlocal terminal_tree_anchor_fiber_checks
            nonlocal terminal_tree_productive_anchor_fiber_checks
            nonlocal terminal_tree_anchor_fiber_labels
            nonlocal terminal_tree_productive_anchor_fiber_labels
            nonlocal terminal_tree_anchor_fiber_max_size
            nonlocal terminal_tree_productive_anchor_fiber_max_size
            nonlocal terminal_tree_mode_rank_checks
            nonlocal terminal_tree_productive_mode_rank_checks
            nonlocal terminal_tree_mode_peeling_checks
            nonlocal terminal_tree_productive_mode_peeling_checks
            nonlocal terminal_tree_mode_annihilator_checks
            nonlocal terminal_tree_productive_mode_annihilator_checks
            nonlocal terminal_tree_boundary_alias_checks
            nonlocal terminal_tree_productive_boundary_alias_checks
            nonlocal terminal_tree_boundary_aliases
            nonlocal terminal_tree_productive_boundary_aliases
            nonlocal terminal_tree_boundary_scalar_fit_candidate_checks
            nonlocal terminal_tree_productive_boundary_scalar_fit_candidate_checks
            nonlocal terminal_tree_boundary_scalar_fits
            nonlocal terminal_tree_productive_boundary_scalar_fits
            nonlocal terminal_tree_boundary_root_linear_checks
            nonlocal terminal_tree_productive_boundary_root_linear_checks
            nonlocal terminal_tree_boundary_root_linear_hits
            nonlocal terminal_tree_productive_boundary_root_linear_hits
            nonlocal terminal_tree_boundary_max_fiber_size
            nonlocal terminal_tree_productive_boundary_max_fiber_size
            nonlocal terminal_tree_multiflag_cores
            nonlocal max_nonzero_terminal_bottom_supports
            nonlocal max_nonzero_terminal_support_bound_slack
            nonlocal max_nonzero_terminal_tree_count
            nonlocal max_nonzero_terminal_tree_branch_vertices
            nonlocal max_nonzero_terminal_tree_branch_pairs
            nonlocal max_nonzero_terminal_tree_productive_branch_pairs
            nonlocal max_nonzero_terminal_tree_mode_packets
            nonlocal max_nonzero_terminal_tree_productive_mode_packets
            nonlocal max_nonzero_terminal_tree_visible_packet_fiber_size
            nonlocal max_nonzero_terminal_tree_productive_visible_packet_fiber_size
            nonlocal max_nonzero_terminal_tree_mode_size
            nonlocal max_nonzero_terminal_tree_mode_rank_checks
            nonlocal max_nonzero_terminal_tree_mode_rank_size
            nonlocal max_nonzero_terminal_tree_mode_peeling_checks
            nonlocal max_nonzero_terminal_tree_mode_annihilator_checks
            nonlocal max_nonzero_terminal_tree_multiflag_cores

            terminal_supports: set[tuple[int, ...]] = set()
            terminal_paths_by_core: Counter[tuple[int, ...]] = Counter()
            visible_packet_productions: Counter[
                tuple[int, tuple[tuple[int, int], ...]]
            ] = Counter()
            productive_visible_packet_productions: Counter[
                tuple[int, tuple[tuple[int, int], ...]]
            ] = Counter()
            visible_packet_anchor_bases: dict[
                tuple[int, tuple[tuple[int, int], ...]],
                list[tuple[int, ...]],
            ] = {}
            productive_visible_packet_anchor_bases: dict[
                tuple[int, tuple[tuple[int, int], ...]],
                list[tuple[int, ...]],
            ] = {}
            anchor_split_fibers: dict[
                tuple[int, tuple[int, ...]],
                list[tuple[int, ...]],
            ] = {}
            productive_anchor_split_fibers: dict[
                tuple[int, tuple[int, ...]],
                list[tuple[int, ...]],
            ] = {}
            total_split_support_fibers: dict[
                tuple[int, tuple[int, ...]],
                list[tuple[int, ...]],
            ] = {}
            productive_total_split_support_fibers: dict[
                tuple[int, tuple[int, ...]],
                list[tuple[int, ...]],
            ] = {}
            total_split_supports: set[tuple[int, ...]] = set()
            productive_total_split_supports: set[tuple[int, ...]] = set()
            marked_split_supports: dict[
                tuple[int, ...],
                dict[int, int],
            ] = {}

            def marked_roots_for_split_support(
                total_support: tuple[int, ...],
            ) -> dict[int, int]:
                cached = marked_split_supports.get(total_support)
                if cached is not None:
                    return cached
                marked_scalars: dict[int, int] = {}
                for root_index in total_support:
                    root = domain[root_index]
                    boundary_support = tuple(
                        index
                        for index in total_support
                        if index != root_index
                    )
                    boundary_vector = hankel_apply(
                        syn,
                        cached_locator(boundary_support),
                        t + 1,
                        p,
                    )
                    expected_boundary = tuple(
                        boundary_vector[0] * pow(root, row, p) % p
                        for row in range(t + 1)
                    )
                    if boundary_vector != expected_boundary:
                        raise AssertionError(
                            {
                                "kind": (
                                    "terminal-split-support-marked-"
                                    "boundary-line-failed"
                                ),
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "total_split_support": list(total_support),
                                "exit_root": root_index,
                                "boundary_vector": list(boundary_vector),
                                "expected_boundary": list(
                                    expected_boundary
                                ),
                            }
                        )
                    scalar = boundary_vector[0] % p
                    if scalar:
                        marked_scalars[root_index] = scalar
                marked_split_supports[total_support] = marked_scalars
                return marked_scalars

            def marked_subset_packet(
                total_support: tuple[int, ...],
                candidate_modes: tuple[int, ...],
                marked_roots: dict[int, int],
            ) -> tuple[tuple[int, ...], list[int]]:
                candidate_mode_set = set(candidate_modes)
                candidate_anchor = tuple(
                    index
                    for index in total_support
                    if index not in candidate_mode_set
                )
                expected = []
                for row in range(t + len(candidate_modes)):
                    total = 0
                    for root_index in candidate_modes:
                        root = domain[root_index]
                        denominator = 1
                        for other_root_index in candidate_modes:
                            if other_root_index == root_index:
                                continue
                            denominator = (
                                denominator
                                * (root - domain[other_root_index])
                            ) % p
                        amplitude = (
                            marked_roots[root_index]
                            * pow(denominator, -1, p)
                        ) % p
                        total += amplitude * pow(root, row, p)
                    expected.append(total % p)
                return candidate_anchor, expected

            def mixed_marked_subset_packet(
                total_support: tuple[int, ...],
                deleted_unmarked: tuple[int, ...],
                candidate_modes: tuple[int, ...],
                marked_roots: dict[int, int],
            ) -> tuple[tuple[int, ...], list[int]]:
                removed = set(deleted_unmarked) | set(candidate_modes)
                candidate_anchor = tuple(
                    index for index in total_support if index not in removed
                )
                expected = []
                for row in range(
                    t + len(deleted_unmarked) + len(candidate_modes)
                ):
                    total = 0
                    for root_index in candidate_modes:
                        root = domain[root_index]
                        denominator = 1
                        for deleted_index in deleted_unmarked:
                            denominator = (
                                denominator
                                * (root - domain[deleted_index])
                            ) % p
                        for other_root_index in candidate_modes:
                            if other_root_index == root_index:
                                continue
                            denominator = (
                                denominator
                                * (root - domain[other_root_index])
                            ) % p
                        amplitude = (
                            marked_roots[root_index]
                            * pow(denominator, -1, p)
                        ) % p
                        total += amplitude * pow(root, row, p)
                    expected.append(total % p)
                return candidate_anchor, expected

            audit_terminal_paths = 0
            for core in active_cores:
                if not core:
                    continue
                for deletion_order in itertools.permutations(core):
                    case_filtration_paths += 1
                    filtration_path_checks += 1
                    current_fixed = list(fixed_roots)
                    current_core = tuple(core)
                    stopped = False
                    for depth, deleted_root_index in enumerate(
                        deletion_order,
                        start=1,
                    ):
                        current_values = [
                            domain[index] for index in current_fixed
                        ]
                        diff_syn = iterated_root_difference_syndrome(
                            syn,
                            current_values,
                            p,
                        )
                        boundary_core = tuple(
                            entry
                            for entry in current_core
                            if entry != deleted_root_index
                        )
                        boundary_vector = hankel_apply(
                            diff_syn,
                            cached_locator(boundary_core),
                            t + 1,
                            p,
                        )
                        if not any(boundary_vector):
                            if boundary_vector[0] != 0:
                                case_filtration_path_defect += 1
                                raise AssertionError(
                                    {
                                        "kind": (
                                            "zero-boundary-nonzero-"
                                            "first-scalar"
                                        ),
                                        "p": p,
                                        "k": k,
                                        "syndrome": list(syn),
                                        "fixed_roots": list(fixed_roots),
                                        "core": list(core),
                                        "deletion_order": list(deletion_order),
                                        "depth": depth,
                                        "boundary_core": list(boundary_core),
                                        "boundary_vector": list(boundary_vector),
                                    }
                                )
                            filtration_zero_stop_depth_histogram[depth] += 1
                            case_zero_stop_filtration_paths += 1
                            filtration_zero_stop_paths += 1
                            stopped = True
                            break
                        deleted_root = domain[deleted_root_index]
                        if boundary_vector[0] == 0 or any(
                            boundary_vector[row + 1]
                            != deleted_root * boundary_vector[row] % p
                            for row in range(t)
                        ):
                            case_filtration_path_defect += 1
                            raise AssertionError(
                                {
                                    "kind": (
                                        "filtration-path-"
                                        "nonzero-step-not-root-marked"
                                    ),
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "fixed_roots": list(fixed_roots),
                                    "core": list(core),
                                    "deletion_order": list(deletion_order),
                                    "depth": depth,
                                    "deleted_root": deleted_root_index,
                                    "deleted_root_value": deleted_root,
                                    "boundary_core": list(boundary_core),
                                    "boundary_vector": list(boundary_vector),
                                }
                            )
                        current_fixed.append(deleted_root_index)
                        current_core = boundary_core
                        case_filtration_nonzero_scalar_steps += 1
                        filtration_nonzero_scalar_steps += 1
                    if stopped:
                        continue
                    terminal_values = [domain[index] for index in current_fixed]
                    terminal_syn = iterated_root_difference_syndrome(
                        syn,
                        terminal_values,
                        p,
                    )
                    if not hankel_annihilates(
                        terminal_syn,
                        cached_locator(current_core),
                        t,
                        p,
                    ):
                        case_filtration_path_defect += 1
                        raise AssertionError(
                            {
                                "kind": "filtration-terminal-condition-failed",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "core": list(core),
                                "deletion_order": list(deletion_order),
                                "terminal_core": list(current_core),
                                "terminal_syndrome": list(terminal_syn),
                            }
                        )
                    canonical_values = [
                        domain[index] for index in sorted((*fixed_roots, *core))
                    ]
                    canonical_terminal_syn = iterated_root_difference_syndrome(
                        syn,
                        canonical_values,
                        p,
                    )
                    if not hankel_annihilates(
                        canonical_terminal_syn,
                        cached_locator(()),
                        t,
                        p,
                    ):
                        case_filtration_path_defect += 1
                        raise AssertionError(
                            {
                                "kind": (
                                    "terminal-bottom-support-"
                                    "order-independence-failed"
                                ),
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "core": list(core),
                                "deletion_order": list(deletion_order),
                                "canonical_values": canonical_values,
                                "terminal_syndrome": list(terminal_syn),
                                "canonical_terminal_syndrome": list(
                                    canonical_terminal_syn
                                ),
                            }
                        )
                    terminal_supports.add(core)
                    terminal_paths_by_core[core] += 1
                    audit_terminal_paths += 1
                    case_terminal_filtration_paths += 1
                    filtration_terminal_paths += 1

            def terminal_deletion_tree(
                current_fixed: tuple[int, ...],
                current_core: tuple[int, ...],
            ) -> tuple[
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
            ]:
                nonlocal terminal_tree_boundary_alias_checks
                nonlocal terminal_tree_productive_boundary_alias_checks
                nonlocal terminal_tree_boundary_aliases
                nonlocal terminal_tree_productive_boundary_aliases
                nonlocal terminal_tree_boundary_scalar_fit_candidate_checks
                nonlocal terminal_tree_productive_boundary_scalar_fit_candidate_checks
                nonlocal terminal_tree_boundary_scalar_fits
                nonlocal terminal_tree_productive_boundary_scalar_fits
                nonlocal terminal_tree_boundary_root_linear_checks
                nonlocal terminal_tree_productive_boundary_root_linear_checks
                nonlocal terminal_tree_boundary_root_linear_hits
                nonlocal terminal_tree_productive_boundary_root_linear_hits
                nonlocal terminal_tree_boundary_root_linear_by_support
                nonlocal terminal_tree_boundary_support_unique
                nonlocal terminal_tree_productive_boundary_support_unique
                nonlocal terminal_tree_boundary_max_fiber_size
                nonlocal terminal_tree_productive_boundary_max_fiber_size
                nonlocal terminal_tree_mode_sizes_seen
                nonlocal terminal_tree_boundary_mode_sizes_seen
                nonlocal terminal_tree_mode_anchor_reconstruction_checks
                nonlocal terminal_tree_productive_mode_anchor_reconstruction_checks
                nonlocal terminal_tree_anchor_base_image_checks
                nonlocal terminal_tree_productive_anchor_base_image_checks
                nonlocal terminal_tree_anchor_base_one_exchange_core_checks
                nonlocal terminal_tree_productive_anchor_base_one_exchange_core_checks
                nonlocal terminal_tree_anchor_base_one_exchange_kernel_hits
                nonlocal terminal_tree_productive_anchor_base_one_exchange_kernel_hits
                nonlocal terminal_tree_anchor_split_support_checks
                nonlocal terminal_tree_productive_anchor_split_support_checks
                nonlocal terminal_tree_anchor_split_boundary_checks
                nonlocal terminal_tree_productive_anchor_split_boundary_checks
                nonlocal terminal_tree_anchor_split_roundtrip_checks
                nonlocal terminal_tree_productive_anchor_split_roundtrip_checks
                nonlocal terminal_tree_anchor_split_absorption_checks
                nonlocal terminal_tree_productive_anchor_split_absorption_checks
                nonlocal terminal_tree_anchor_split_proper_absorption_checks
                nonlocal terminal_tree_productive_anchor_split_proper_absorption_checks
                nonlocal terminal_tree_anchor_split_ordered_mode_flags
                nonlocal terminal_tree_productive_anchor_split_ordered_mode_flags

                if not current_core:
                    return (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                current_values = [domain[index] for index in current_fixed]
                diff_syn = iterated_root_difference_syndrome(
                    syn,
                    current_values,
                    p,
                )
                if not hankel_annihilates(
                    diff_syn,
                    cached_locator(current_core),
                    t,
                    p,
                ):
                    raise AssertionError(
                        {
                            "kind": "terminal-tree-inactive-vertex",
                            "p": p,
                            "k": k,
                            "syndrome": list(syn),
                            "fixed_roots": list(fixed_roots),
                            "current_fixed": list(current_fixed),
                            "current_core": list(current_core),
                        }
                    )
                nonzero_children: list[tuple[int, tuple[int, ...], int]] = []
                for deleted_root_index in current_core:
                    boundary_core = tuple(
                        entry
                        for entry in current_core
                        if entry != deleted_root_index
                    )
                    boundary_vector = hankel_apply(
                        diff_syn,
                        cached_locator(boundary_core),
                        t + 1,
                        p,
                    )
                    if not any(boundary_vector):
                        continue
                    deleted_root = domain[deleted_root_index]
                    if boundary_vector[0] == 0 or any(
                        boundary_vector[row + 1]
                        != deleted_root * boundary_vector[row] % p
                        for row in range(t)
                    ):
                        raise AssertionError(
                            {
                                "kind": (
                                    "terminal-tree-nonzero-edge-"
                                    "not-root-marked"
                                ),
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "current_fixed": list(current_fixed),
                                "current_core": list(current_core),
                                "deleted_root": deleted_root_index,
                                "deleted_root_value": deleted_root,
                                "boundary_core": list(boundary_core),
                                "boundary_vector": list(boundary_vector),
                            }
                        )
                    child_values = [
                        domain[index]
                        for index in (*current_fixed, deleted_root_index)
                    ]
                    child_syn = iterated_root_difference_syndrome(
                        syn,
                        child_values,
                        p,
                    )
                    if not hankel_annihilates(
                        child_syn,
                        cached_locator(boundary_core),
                        t,
                        p,
                    ):
                        raise AssertionError(
                            {
                                "kind": "terminal-tree-child-inactive",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "current_fixed": list(current_fixed),
                                "current_core": list(current_core),
                                "deleted_root": deleted_root_index,
                                "boundary_core": list(boundary_core),
                                "child_syndrome": list(child_syn),
                            }
                        )
                    nonzero_children.append(
                        (
                            deleted_root_index,
                            boundary_core,
                            boundary_vector[0],
                        )
                    )
                child_results: list[tuple[int, int, tuple[int, ...], int]] = []
                terminal_count = 0
                branch_count = 1 if len(nonzero_children) >= 2 else 0
                branch_pair_count = 0
                productive_branch_pair_count = 0
                mode_packet_count = 0
                productive_mode_packet_count = 0
                max_mode_size = 0
                mode_rank_count = 0
                productive_mode_rank_count = 0
                max_mode_rank_size = 0
                mode_peeling_count = 0
                productive_mode_peeling_count = 0
                mode_annihilator_count = 0
                productive_mode_annihilator_count = 0
                for deleted_root_index, boundary_core, scalar in nonzero_children:
                    (
                        child_count,
                        child_branches,
                        child_branch_pairs,
                        child_productive_pairs,
                        child_mode_packets,
                        child_productive_mode_packets,
                        child_max_mode_size,
                        child_mode_rank_checks,
                        child_productive_mode_rank_checks,
                        child_max_mode_rank_size,
                        child_mode_peeling_checks,
                        child_productive_mode_peeling_checks,
                        child_mode_annihilator_checks,
                        child_productive_mode_annihilator_checks,
                    ) = terminal_deletion_tree(
                        (*current_fixed, deleted_root_index),
                        boundary_core,
                    )
                    child_results.append(
                        (
                            deleted_root_index,
                            child_count,
                            boundary_core,
                            scalar,
                        )
                    )
                    terminal_count += child_count
                    branch_count += child_branches
                    branch_pair_count += child_branch_pairs
                    productive_branch_pair_count += child_productive_pairs
                    mode_packet_count += child_mode_packets
                    productive_mode_packet_count += child_productive_mode_packets
                    max_mode_size = max(max_mode_size, child_max_mode_size)
                    mode_rank_count += child_mode_rank_checks
                    productive_mode_rank_count += (
                        child_productive_mode_rank_checks
                    )
                    max_mode_rank_size = max(
                        max_mode_rank_size,
                        child_max_mode_rank_size,
                    )
                    mode_peeling_count += child_mode_peeling_checks
                    productive_mode_peeling_count += (
                        child_productive_mode_peeling_checks
                    )
                    mode_annihilator_count += child_mode_annihilator_checks
                    productive_mode_annihilator_count += (
                        child_productive_mode_annihilator_checks
                    )
                if len(child_results) >= 2:
                    child_root_indices = {
                        result[0] for result in child_results
                    }
                    lower_core = tuple(
                        entry
                        for entry in current_core
                        if entry not in child_root_indices
                    )
                    mode_count = len(child_results)
                    lower_vector = hankel_apply(
                        diff_syn,
                        cached_locator(lower_core),
                        t + mode_count,
                        p,
                    )
                    expected = []
                    mode_data: list[tuple[int, int, int, int, int]] = []
                    for row in range(t + mode_count):
                        total = 0
                        for root_index, _child_count, _boundary_core, scalar in (
                            child_results
                        ):
                            root = domain[root_index]
                            denominator = 1
                            for other_root_index in child_root_indices:
                                if other_root_index == root_index:
                                    continue
                                denominator = (
                                    denominator
                                    * (root - domain[other_root_index])
                                ) % p
                            total += (
                                scalar
                                * pow(root, row, p)
                                * pow(denominator, -1, p)
                            )
                            if row == 0:
                                mode_data.append(
                                    (
                                        root_index,
                                        root,
                                        _child_count,
                                        scalar,
                                        scalar * pow(denominator, -1, p) % p,
                                    )
                                )
                        expected.append(total % p)
                    mode_packet_count += 1
                    max_mode_size = max(max_mode_size, mode_count)
                    terminal_tree_mode_sizes_seen.add(mode_count)
                    terminal_tree_mode_size_histogram[mode_count] += 1
                    productive_children = sum(
                        1 for _root, child_count, _core, _scalar in child_results
                        if child_count
                    )
                    if productive_children >= 2:
                        productive_mode_packet_count += 1
                        terminal_tree_productive_mode_size_histogram[
                            mode_count
                        ] += 1
                    if lower_vector != tuple(expected):
                        raise AssertionError(
                            {
                                "kind": "terminal-branch-mode-packet-failed",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "current_fixed": list(current_fixed),
                                "current_core": list(current_core),
                                "exit_roots": [
                                    root_index
                                    for root_index, _count, _core, _scalar in (
                                        child_results
                                    )
                                ],
                                "lower_core": list(lower_core),
                                "lower_vector": list(lower_vector),
                                "expected": expected,
                            }
                        )
                    anchor_base = tuple(
                        sorted((*current_fixed, *lower_core))
                    )
                    if set(anchor_base) & child_root_indices:
                        raise AssertionError(
                            {
                                "kind": (
                                    "terminal-branch-anchor-base-overlaps-"
                                    "modes"
                                ),
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "current_fixed": list(current_fixed),
                                "current_core": list(current_core),
                                "lower_core": list(lower_core),
                                "anchor_base": list(anchor_base),
                                "exit_roots": sorted(child_root_indices),
                            }
                        )
                    anchor_base_vector = hankel_apply(
                        syn,
                        cached_locator(anchor_base),
                        t + mode_count,
                        p,
                    )
                    if anchor_base_vector != lower_vector:
                        raise AssertionError(
                            {
                                "kind": (
                                    "terminal-branch-anchor-base-image-"
                                    "failed"
                                ),
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "current_fixed": list(current_fixed),
                                "current_core": list(current_core),
                                "lower_core": list(lower_core),
                                "anchor_base": list(anchor_base),
                                "anchor_base_vector": list(
                                    anchor_base_vector
                                ),
                                "lower_vector": list(lower_vector),
                            }
                        )
                    terminal_tree_anchor_base_image_checks += 1
                    if productive_children >= 2:
                        terminal_tree_productive_anchor_base_image_checks += 1
                    total_split_support = tuple(
                        sorted((*anchor_base, *child_root_indices))
                    )
                    total_split_vector = hankel_apply(
                        syn,
                        cached_locator(total_split_support),
                        t,
                        p,
                    )
                    if any(total_split_vector):
                        raise AssertionError(
                            {
                                "kind": (
                                    "terminal-branch-anchor-split-"
                                    "support-inactive"
                                ),
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "current_fixed": list(current_fixed),
                                "current_core": list(current_core),
                                "anchor_base": list(anchor_base),
                                "exit_roots": sorted(child_root_indices),
                                "total_split_support": list(
                                    total_split_support
                                ),
                                "total_split_vector": list(
                                    total_split_vector
                                ),
                            }
                        )
                    terminal_tree_anchor_split_support_checks += 1
                    if productive_children >= 2:
                        terminal_tree_productive_anchor_split_support_checks += (
                            1
                        )
                    marked_roots = marked_roots_for_split_support(
                        total_split_support
                    )
                    missing_marked_modes = sorted(
                        child_root_indices - set(marked_roots)
                    )
                    if missing_marked_modes:
                        raise AssertionError(
                            {
                                "kind": (
                                    "terminal-split-support-mode-not-"
                                    "marked"
                                ),
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "anchor_base": list(anchor_base),
                                "exit_roots": sorted(child_root_indices),
                                "total_split_support": list(
                                    total_split_support
                                ),
                                "missing_marked_modes": missing_marked_modes,
                                "marked_roots": sorted(marked_roots),
                            }
                        )
                    for (
                        root_index,
                        root,
                        _child_count,
                        scalar,
                        _amplitude,
                    ) in mode_data:
                        boundary_support = tuple(
                            sorted(
                                (
                                    *anchor_base,
                                    *(
                                        other_root_index
                                        for other_root_index in child_root_indices
                                        if other_root_index != root_index
                                    ),
                                )
                            )
                        )
                        boundary_vector = hankel_apply(
                            syn,
                            cached_locator(boundary_support),
                            t + 1,
                            p,
                        )
                        expected_boundary = tuple(
                            scalar * pow(root, row, p) % p
                            for row in range(t + 1)
                        )
                        if boundary_vector != expected_boundary:
                            raise AssertionError(
                                {
                                    "kind": (
                                        "terminal-branch-anchor-split-"
                                        "boundary-failed"
                                    ),
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "fixed_roots": list(fixed_roots),
                                    "current_fixed": list(current_fixed),
                                    "current_core": list(current_core),
                                    "anchor_base": list(anchor_base),
                                    "boundary_support": list(
                                        boundary_support
                                    ),
                                    "exit_root": root_index,
                                    "scalar": scalar,
                                    "boundary_vector": list(
                                        boundary_vector
                                    ),
                                    "expected_boundary": list(
                                        expected_boundary
                                    ),
                                }
                            )
                        terminal_tree_anchor_split_boundary_checks += 1
                        if productive_children >= 2:
                            terminal_tree_productive_anchor_split_boundary_checks += (
                                1
                            )
                    split_roundtrip_vector = tuple(expected)
                    if anchor_base_vector != split_roundtrip_vector:
                        raise AssertionError(
                            {
                                "kind": (
                                    "terminal-branch-anchor-split-"
                                    "roundtrip-failed"
                                ),
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "current_fixed": list(current_fixed),
                                "current_core": list(current_core),
                                "anchor_base": list(anchor_base),
                                "exit_roots": sorted(child_root_indices),
                                "anchor_base_vector": list(
                                    anchor_base_vector
                                ),
                                "roundtrip_vector": list(
                                    split_roundtrip_vector
                                ),
                            }
                        )
                    terminal_tree_anchor_split_roundtrip_checks += 1
                    if productive_children >= 2:
                        terminal_tree_productive_anchor_split_roundtrip_checks += (
                            1
                        )
                    anchor_fiber_key = (mode_count, anchor_base)
                    anchor_fiber_support = tuple(sorted(child_root_indices))
                    anchor_split_fibers.setdefault(
                        anchor_fiber_key,
                        [],
                    ).append(anchor_fiber_support)
                    if productive_children >= 2:
                        productive_anchor_split_fibers.setdefault(
                            anchor_fiber_key,
                            [],
                        ).append(anchor_fiber_support)
                    total_split_support_fiber_key = (
                        mode_count,
                        total_split_support,
                    )
                    total_split_supports.add(total_split_support)
                    total_split_support_fibers.setdefault(
                        total_split_support_fiber_key,
                        [],
                    ).append(anchor_fiber_support)
                    if productive_children >= 2:
                        productive_total_split_supports.add(
                            total_split_support
                        )
                        productive_total_split_support_fibers.setdefault(
                            total_split_support_fiber_key,
                            [],
                        ).append(anchor_fiber_support)
                    ordered_mode_flags = math.factorial(mode_count)
                    terminal_tree_anchor_split_ordered_mode_flags += (
                        ordered_mode_flags
                    )
                    if productive_children >= 2:
                        terminal_tree_productive_anchor_split_ordered_mode_flags += (
                            ordered_mode_flags
                        )
                    for removed_anchor in anchor_base:
                        common_anchor_core = tuple(
                            anchor
                            for anchor in anchor_base
                            if anchor != removed_anchor
                        )
                        common_anchor_vector = hankel_apply(
                            syn,
                            cached_locator(common_anchor_core),
                            t + mode_count,
                            p,
                        )
                        terminal_tree_anchor_base_one_exchange_core_checks += 1
                        if productive_children >= 2:
                            terminal_tree_productive_anchor_base_one_exchange_core_checks += (
                                1
                            )
                        if not any(common_anchor_vector):
                            terminal_tree_anchor_base_one_exchange_kernel_hits += 1
                            if productive_children >= 2:
                                terminal_tree_productive_anchor_base_one_exchange_kernel_hits += (
                                    1
                                )
                    reconstructed_core = tuple(
                        sorted((*lower_core, *child_root_indices))
                    )
                    if reconstructed_core != current_core:
                        raise AssertionError(
                            {
                                "kind": (
                                    "terminal-branch-anchor-core-"
                                    "reconstruction-failed"
                                ),
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "current_fixed": list(current_fixed),
                                "current_core": list(current_core),
                                "lower_core": list(lower_core),
                                "exit_roots": sorted(child_root_indices),
                                "reconstructed_core": list(
                                    reconstructed_core
                                ),
                            }
                        )
                    for root_index, root, _child_count, scalar, amplitude in (
                        mode_data
                    ):
                        denominator = 1
                        for other_root_index in child_root_indices:
                            if other_root_index == root_index:
                                continue
                            denominator = (
                                denominator
                                * (root - domain[other_root_index])
                            ) % p
                        reconstructed_scalar = amplitude * denominator % p
                        if reconstructed_scalar != scalar:
                            raise AssertionError(
                                {
                                    "kind": (
                                        "terminal-branch-anchor-scalar-"
                                        "reconstruction-failed"
                                    ),
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "fixed_roots": list(fixed_roots),
                                    "current_fixed": list(current_fixed),
                                    "current_core": list(current_core),
                                    "lower_core": list(lower_core),
                                    "exit_root": root_index,
                                    "amplitude": amplitude,
                                    "scalar": scalar,
                                    "reconstructed_scalar": (
                                        reconstructed_scalar
                                    ),
                                }
                            )
                    terminal_tree_mode_anchor_reconstruction_checks += 1
                    if productive_children >= 2:
                        terminal_tree_productive_mode_anchor_reconstruction_checks += (
                            1
                        )
                    visible_packet_label = (
                        mode_count,
                        tuple(
                            sorted(
                                (root_index, amplitude)
                                for (
                                    root_index,
                                    _root,
                                    _child_count,
                                    _scalar,
                                    amplitude,
                                ) in mode_data
                            )
                        ),
                    )
                    visible_packet_productions[visible_packet_label] += 1
                    visible_packet_anchor_bases.setdefault(
                        visible_packet_label,
                        [],
                    ).append(anchor_base)
                    if productive_children >= 2:
                        productive_visible_packet_productions[
                            visible_packet_label
                        ] += 1
                        productive_visible_packet_anchor_bases.setdefault(
                            visible_packet_label,
                            [],
                        ).append(anchor_base)
                    if 2 * mode_count - 1 <= len(lower_vector):
                        moment_matrix = tuple(
                            tuple(
                                lower_vector[row + column]
                                for column in range(mode_count)
                            )
                            for row in range(mode_count)
                        )
                        moment_determinant = determinant_mod(moment_matrix, p)
                        roots = [
                            domain[root_index]
                            for root_index, _count, _core, _scalar in (
                                child_results
                            )
                        ]
                        amplitude_product = 1
                        for root_index, _count, _core, scalar in child_results:
                            root = domain[root_index]
                            denominator = 1
                            for other_root_index in child_root_indices:
                                if other_root_index == root_index:
                                    continue
                                denominator = (
                                    denominator
                                    * (root - domain[other_root_index])
                                ) % p
                            amplitude_product = (
                                amplitude_product
                                * scalar
                                * pow(denominator, -1, p)
                            ) % p
                        vandermonde = 1
                        for left_root, right_root in itertools.combinations(
                            roots,
                            2,
                        ):
                            vandermonde = (
                                vandermonde * (right_root - left_root)
                            ) % p
                        expected_determinant = (
                            amplitude_product * vandermonde * vandermonde
                        ) % p
                        mode_rank_count += 1
                        max_mode_rank_size = max(
                            max_mode_rank_size,
                            mode_count,
                        )
                        terminal_tree_mode_rank_size_histogram[mode_count] += 1
                        if productive_children >= 2:
                            productive_mode_rank_count += 1
                        if (
                            moment_determinant != expected_determinant
                            or moment_determinant == 0
                        ):
                            raise AssertionError(
                                {
                                    "kind": (
                                        "terminal-branch-mode-rank-"
                                        "certificate-failed"
                                    ),
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "fixed_roots": list(fixed_roots),
                                    "current_fixed": list(current_fixed),
                                    "current_core": list(current_core),
                                    "exit_roots": [
                                        root_index
                                        for root_index, _count, _core, _scalar in (
                                            child_results
                                        )
                                    ],
                                    "lower_core": list(lower_core),
                                    "moment_matrix": [
                                        list(row) for row in moment_matrix
                                    ],
                                    "moment_determinant": moment_determinant,
                                    "expected_determinant": (
                                        expected_determinant
                                    ),
                                }
                            )
                        if 2 * mode_count <= len(lower_vector):
                            rhs = tuple(
                                (-lower_vector[row + mode_count]) % p
                                for row in range(mode_count)
                            )
                            recovered = (
                                solve_square_mod(moment_matrix, rhs, p) + (1,)
                            )
                            mode_locator = cached_locator(
                                tuple(sorted(child_root_indices))
                            )
                            mode_annihilator_count += 1
                            terminal_tree_mode_annihilator_size_histogram[
                                mode_count
                            ] += 1
                            if productive_children >= 2:
                                productive_mode_annihilator_count += 1
                            if recovered != mode_locator:
                                raise AssertionError(
                                    {
                                        "kind": (
                                            "terminal-branch-mode-"
                                            "annihilator-recovery-failed"
                                        ),
                                        "p": p,
                                        "k": k,
                                        "syndrome": list(syn),
                                        "fixed_roots": list(fixed_roots),
                                        "current_fixed": list(current_fixed),
                                        "current_core": list(current_core),
                                        "exit_roots": [
                                            root_index
                                            for (
                                                root_index,
                                                _count,
                                                _core,
                                                _scalar,
                                            ) in child_results
                                        ],
                                        "lower_core": list(lower_core),
                                        "recovered": list(recovered),
                                        "mode_locator": list(mode_locator),
                                    }
                                )
                        elif len(lower_vector) == 2 * mode_count - 1:
                            terminal_tree_boundary_mode_sizes_seen.add(
                                mode_count
                            )
                            aliases: list[tuple[int, ...]] = []
                            scalar_fit_count = 0
                            mode_amplitude_by_index = {
                                root_index: amplitude
                                for (
                                    root_index,
                                    _root,
                                    _child_count,
                                    _scalar,
                                    amplitude,
                                ) in mode_data
                            }
                            mode_scalar_by_index = {
                                root_index: scalar
                                for (
                                    root_index,
                                    _root,
                                    _child_count,
                                    scalar,
                                    _amplitude,
                                ) in mode_data
                            }
                            for candidate in itertools.combinations(
                                range(n),
                                mode_count,
                            ):
                                candidate_set = set(candidate)
                                if candidate_set == child_root_indices:
                                    continue
                                candidate_roots = [
                                    domain[index] for index in candidate
                                ]
                                amplitudes = sparse_moment_amplitudes(
                                    candidate_roots,
                                    lower_vector,
                                    p,
                                )
                                is_alias = (
                                    amplitudes is not None
                                    and all(amplitudes)
                                )
                                if child_root_indices & candidate_set:
                                    if is_alias:
                                        raise AssertionError(
                                            {
                                                "kind": (
                                                    "terminal-branch-"
                                                    "boundary-overlapping-"
                                                    "alias"
                                                ),
                                                "p": p,
                                                "k": k,
                                                "syndrome": list(syn),
                                                "fixed_roots": list(
                                                    fixed_roots
                                                ),
                                                "current_fixed": list(
                                                    current_fixed
                                                ),
                                                "current_core": list(
                                                    current_core
                                                ),
                                                "exit_roots": sorted(
                                                    child_root_indices
                                                ),
                                                "alias_roots": list(candidate),
                                                "lower_vector": list(
                                                    lower_vector
                                                ),
                                                "alias_amplitudes": list(
                                                    amplitudes
                                                ),
                                            }
                                        )
                                    continue
                                scalar_products = set()
                                for root_index in child_root_indices:
                                    root = domain[root_index]
                                    locator_value = 1
                                    for candidate_index in candidate:
                                        locator_value = (
                                            locator_value
                                            * (root - domain[candidate_index])
                                        ) % p
                                    scalar_products.add(
                                        mode_scalar_by_index[root_index]
                                        * locator_value
                                        % p
                                    )
                                scalar_fit = (
                                    len(scalar_products) == 1
                                    and 0 not in scalar_products
                                )
                                terminal_tree_boundary_scalar_fit_candidate_checks += (
                                    1
                                )
                                if productive_children >= 2:
                                    terminal_tree_productive_boundary_scalar_fit_candidate_checks += (
                                        1
                                    )
                                if scalar_fit:
                                    scalar_fit_count += 1
                                if scalar_fit != is_alias:
                                    raise AssertionError(
                                        {
                                            "kind": (
                                                "terminal-branch-boundary-"
                                                "scalar-fit-mismatch"
                                            ),
                                            "p": p,
                                            "k": k,
                                            "syndrome": list(syn),
                                            "fixed_roots": list(fixed_roots),
                                            "current_fixed": list(
                                                current_fixed
                                            ),
                                            "current_core": list(
                                                current_core
                                            ),
                                            "exit_roots": sorted(
                                                child_root_indices
                                            ),
                                            "alias_roots": list(candidate),
                                            "scalar_products": sorted(
                                                scalar_products
                                            ),
                                            "is_alias": is_alias,
                                            "alias_amplitudes": (
                                                None
                                                if amplitudes is None
                                                else list(amplitudes)
                                            ),
                                        }
                                    )
                                if not is_alias:
                                    continue
                                union = child_root_indices | candidate_set

                                def derivative_at(root_index: int) -> int:
                                    root = domain[root_index]
                                    derivative = 1
                                    for other_root_index in union:
                                        if other_root_index == root_index:
                                            continue
                                        derivative = (
                                            derivative
                                            * (root - domain[other_root_index])
                                        ) % p
                                    return derivative

                                mu_values = {
                                    mode_amplitude_by_index[root_index]
                                    * derivative_at(root_index)
                                    % p
                                    for root_index in child_root_indices
                                }
                                if len(mu_values) != 1 or 0 in mu_values:
                                    raise AssertionError(
                                        {
                                            "kind": (
                                                "terminal-branch-boundary-"
                                                "alias-kernel-weight-failed"
                                            ),
                                            "p": p,
                                            "k": k,
                                            "syndrome": list(syn),
                                            "fixed_roots": list(fixed_roots),
                                            "current_fixed": list(
                                                current_fixed
                                            ),
                                            "current_core": list(
                                                current_core
                                            ),
                                            "exit_roots": sorted(
                                                child_root_indices
                                            ),
                                            "alias_roots": list(candidate),
                                            "mu_values": sorted(mu_values),
                                        }
                                    )
                                mu = next(iter(mu_values))
                                for candidate_index, amplitude in zip(
                                    candidate,
                                    amplitudes,
                                ):
                                    expected_amplitude = (
                                        -mu
                                        * pow(
                                            derivative_at(candidate_index),
                                            -1,
                                            p,
                                        )
                                    ) % p
                                    if amplitude != expected_amplitude:
                                        raise AssertionError(
                                            {
                                                "kind": (
                                                    "terminal-branch-"
                                                    "boundary-alias-"
                                                    "amplitude-failed"
                                                ),
                                                "p": p,
                                                "k": k,
                                                "syndrome": list(syn),
                                                "fixed_roots": list(
                                                    fixed_roots
                                                ),
                                                "current_fixed": list(
                                                    current_fixed
                                                ),
                                                "current_core": list(
                                                    current_core
                                                ),
                                                "exit_roots": sorted(
                                                    child_root_indices
                                                ),
                                                "alias_roots": list(
                                                    candidate
                                                ),
                                                "alias_root": (
                                                    candidate_index
                                                ),
                                                "amplitude": amplitude,
                                                "expected_amplitude": (
                                                    expected_amplitude
                                                ),
                                            }
                                        )
                                aliases.append(candidate)
                            terminal_tree_boundary_alias_checks += 1
                            terminal_tree_boundary_aliases += len(aliases)
                            terminal_tree_boundary_alias_histogram[
                                len(aliases)
                            ] += 1
                            fiber_size = 1 + len(aliases)
                            if fiber_size > n // mode_count:
                                raise AssertionError(
                                    {
                                        "kind": (
                                            "terminal-branch-boundary-"
                                            "fiber-size-bound-failed"
                                        ),
                                        "p": p,
                                        "k": k,
                                        "syndrome": list(syn),
                                        "fixed_roots": list(fixed_roots),
                                        "current_fixed": list(current_fixed),
                                        "current_core": list(current_core),
                                        "exit_roots": sorted(
                                            child_root_indices
                                        ),
                                        "aliases": [
                                            list(alias) for alias in aliases
                                        ],
                                        "fiber_size": fiber_size,
                                        "bound": n // mode_count,
                                    }
                                )
                            terminal_tree_boundary_max_fiber_size = max(
                                terminal_tree_boundary_max_fiber_size,
                                fiber_size,
                            )
                            terminal_tree_boundary_fiber_size_histogram[
                                fiber_size
                            ] += 1
                            if productive_children >= 2:
                                terminal_tree_productive_boundary_alias_checks += 1
                                terminal_tree_productive_boundary_aliases += (
                                    len(aliases)
                                )
                                terminal_tree_productive_boundary_alias_histogram[
                                    len(aliases)
                                ] += 1
                                terminal_tree_productive_boundary_max_fiber_size = max(
                                    terminal_tree_productive_boundary_max_fiber_size,
                                    fiber_size,
                                )
                                terminal_tree_productive_boundary_fiber_size_histogram[
                                    fiber_size
                                ] += 1
                            terminal_tree_boundary_scalar_fits += scalar_fit_count
                            terminal_tree_boundary_scalar_fit_histogram[
                                scalar_fit_count
                            ] += 1
                            if productive_children >= 2:
                                terminal_tree_productive_boundary_scalar_fits += (
                                    scalar_fit_count
                                )
                                terminal_tree_productive_boundary_scalar_fit_histogram[
                                    scalar_fit_count
                                ] += 1
                            if n == 2 * mode_count:
                                root_linear_values = {
                                    mode_amplitude_by_index[root_index]
                                    * pow(domain[root_index], -1, p)
                                    % p
                                    for root_index in child_root_indices
                                }
                                root_linear = (
                                    len(root_linear_values) == 1
                                    and 0 not in root_linear_values
                                )
                                terminal_tree_boundary_root_linear_checks += 1
                                terminal_tree_boundary_root_linear_histogram[
                                    int(root_linear)
                                ] += 1
                                if root_linear:
                                    terminal_tree_boundary_root_linear_hits += 1
                                    terminal_tree_boundary_root_linear_by_support[
                                        tuple(sorted(child_root_indices))
                                    ] += 1
                                if productive_children >= 2:
                                    terminal_tree_productive_boundary_root_linear_checks += (
                                        1
                                    )
                                    terminal_tree_productive_boundary_root_linear_histogram[
                                        int(root_linear)
                                    ] += 1
                                    if root_linear:
                                        terminal_tree_productive_boundary_root_linear_hits += (
                                            1
                                        )
                                if root_linear != bool(aliases):
                                    raise AssertionError(
                                        {
                                            "kind": (
                                                "terminal-branch-boundary-"
                                                "root-linear-mismatch"
                                            ),
                                            "p": p,
                                            "k": k,
                                            "syndrome": list(syn),
                                            "fixed_roots": list(fixed_roots),
                                            "current_fixed": list(
                                                current_fixed
                                            ),
                                            "current_core": list(
                                                current_core
                                            ),
                                            "exit_roots": sorted(
                                                child_root_indices
                                            ),
                                            "aliases": [
                                                list(alias)
                                                for alias in aliases
                                            ],
                                            "root_linear_values": sorted(
                                                root_linear_values
                                            ),
                                        }
                                    )
                                if not aliases:
                                    terminal_tree_boundary_support_unique += 1
                                    if productive_children >= 2:
                                        terminal_tree_productive_boundary_support_unique += (
                                            1
                                        )
                    for subset_size in range(1, mode_count + 1):
                        for subset in itertools.combinations(
                            sorted(child_root_indices),
                            subset_size,
                        ):
                            subset_set = set(subset)
                            peeled_core = tuple(sorted((*lower_core, *subset)))
                            row_count = t + mode_count - subset_size
                            peeled_vector = hankel_apply(
                                diff_syn,
                                cached_locator(peeled_core),
                                row_count,
                                p,
                            )
                            peeled_expected = []
                            for row in range(row_count):
                                total = 0
                                for (
                                    root_index,
                                    root,
                                    _child_count,
                                    _scalar,
                                    amplitude,
                                ) in mode_data:
                                    if root_index in subset_set:
                                        continue
                                    subset_locator_value = 1
                                    for subset_root_index in subset:
                                        subset_locator_value = (
                                            subset_locator_value
                                            * (root - domain[subset_root_index])
                                        ) % p
                                    total += (
                                        amplitude
                                        * subset_locator_value
                                        * pow(root, row, p)
                                    )
                                peeled_expected.append(total % p)
                            mode_peeling_count += 1
                            terminal_tree_mode_peeling_subset_size_histogram[
                                subset_size
                            ] += 1
                            if productive_children >= 2:
                                productive_mode_peeling_count += 1
                            if peeled_vector != tuple(peeled_expected) or (
                                subset_size < mode_count
                                and not any(peeled_vector)
                            ):
                                raise AssertionError(
                                    {
                                        "kind": (
                                            "terminal-branch-mode-"
                                            "peeling-failed"
                                        ),
                                        "p": p,
                                        "k": k,
                                        "syndrome": list(syn),
                                        "fixed_roots": list(fixed_roots),
                                        "current_fixed": list(current_fixed),
                                        "current_core": list(current_core),
                                        "exit_roots": sorted(
                                            child_root_indices
                                        ),
                                        "peeled_roots": list(subset),
                                        "peeled_core": list(peeled_core),
                                        "peeled_vector": list(peeled_vector),
                                        "expected": peeled_expected,
                                    }
                                )
                            absorbed_anchor = tuple(
                                sorted((*anchor_base, *subset))
                            )
                            absorbed_vector = hankel_apply(
                                syn,
                                cached_locator(absorbed_anchor),
                                row_count,
                                p,
                            )
                            terminal_tree_anchor_split_absorption_checks += 1
                            if productive_children >= 2:
                                terminal_tree_productive_anchor_split_absorption_checks += (
                                    1
                                )
                            if subset_size < mode_count:
                                terminal_tree_anchor_split_proper_absorption_checks += (
                                    1
                                )
                                if productive_children >= 2:
                                    terminal_tree_productive_anchor_split_proper_absorption_checks += (
                                        1
                                    )
                            if absorbed_vector != tuple(peeled_expected) or (
                                subset_size < mode_count
                                and not any(absorbed_vector)
                            ):
                                raise AssertionError(
                                    {
                                        "kind": (
                                            "terminal-branch-anchor-split-"
                                            "absorption-failed"
                                        ),
                                        "p": p,
                                        "k": k,
                                        "syndrome": list(syn),
                                        "fixed_roots": list(fixed_roots),
                                        "current_fixed": list(current_fixed),
                                        "current_core": list(current_core),
                                        "anchor_base": list(anchor_base),
                                        "absorbed_roots": list(subset),
                                        "absorbed_anchor": list(
                                            absorbed_anchor
                                        ),
                                        "remaining_roots": [
                                            root_index
                                            for root_index in sorted(
                                                child_root_indices - subset_set
                                            )
                                        ],
                                        "absorbed_vector": list(
                                            absorbed_vector
                                        ),
                                        "expected": peeled_expected,
                                    }
                                )
                for left, right in itertools.combinations(child_results, 2):
                    (
                        left_root_index,
                        left_count,
                        _left_boundary_core,
                        left_scalar,
                    ) = left
                    (
                        right_root_index,
                        right_count,
                        _right_boundary_core,
                        right_scalar,
                    ) = right
                    left_root = domain[left_root_index]
                    right_root = domain[right_root_index]
                    lower_core = tuple(
                        entry
                        for entry in current_core
                        if entry not in {left_root_index, right_root_index}
                    )
                    lower_vector = hankel_apply(
                        diff_syn,
                        cached_locator(lower_core),
                        t + 2,
                        p,
                    )
                    denominator = (left_root - right_root) % p
                    expected = tuple(
                        (
                            (
                                left_scalar * pow(left_root, row, p)
                                - right_scalar * pow(right_root, row, p)
                            )
                            * pow(denominator, -1, p)
                        )
                        % p
                        for row in range(t + 2)
                    )
                    branch_pair_count += 1
                    if left_count and right_count:
                        productive_branch_pair_count += 1
                    if lower_vector != expected:
                        raise AssertionError(
                            {
                                "kind": "terminal-branch-pair-two-mode-failed",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "current_fixed": list(current_fixed),
                                "current_core": list(current_core),
                                "left_root": left_root_index,
                                "right_root": right_root_index,
                                "lower_core": list(lower_core),
                                "left_scalar": left_scalar,
                                "right_scalar": right_scalar,
                                "lower_vector": list(lower_vector),
                                "expected": list(expected),
                            }
                        )
                return (
                    terminal_count,
                    branch_count,
                    branch_pair_count,
                    productive_branch_pair_count,
                    mode_packet_count,
                    productive_mode_packet_count,
                    max_mode_size,
                    mode_rank_count,
                    productive_mode_rank_count,
                    max_mode_rank_size,
                    mode_peeling_count,
                    productive_mode_peeling_count,
                    mode_annihilator_count,
                    productive_mode_annihilator_count,
                )

            tree_recursion_defects = 0
            audit_branch_vertices = 0
            audit_branch_pairs = 0
            audit_productive_branch_pairs = 0
            audit_mode_packets = 0
            audit_productive_mode_packets = 0
            audit_mode_rank_checks = 0
            audit_productive_mode_rank_checks = 0
            audit_mode_peeling_checks = 0
            audit_productive_mode_peeling_checks = 0
            audit_mode_annihilator_checks = 0
            audit_productive_mode_annihilator_checks = 0
            audit_multiflag_cores = 0
            for core in active_cores:
                if not core:
                    continue
                (
                    tree_count,
                    branch_count,
                    branch_pair_count,
                    productive_branch_pair_count,
                    mode_packet_count,
                    productive_mode_packet_count,
                    max_mode_size,
                    mode_rank_count,
                    productive_mode_rank_count,
                    max_mode_rank_size,
                    mode_peeling_count,
                    productive_mode_peeling_count,
                    mode_annihilator_count,
                    productive_mode_annihilator_count,
                ) = terminal_deletion_tree(
                    fixed_roots,
                    core,
                )
                terminal_tree_recursion_checks += 1
                terminal_tree_branch_vertices += branch_count
                terminal_tree_branch_pair_checks += branch_pair_count
                terminal_tree_productive_branch_pairs += (
                    productive_branch_pair_count
                )
                terminal_tree_mode_packet_checks += mode_packet_count
                terminal_tree_productive_mode_packets += (
                    productive_mode_packet_count
                )
                terminal_tree_mode_rank_checks += mode_rank_count
                terminal_tree_productive_mode_rank_checks += (
                    productive_mode_rank_count
                )
                terminal_tree_mode_peeling_checks += mode_peeling_count
                terminal_tree_productive_mode_peeling_checks += (
                    productive_mode_peeling_count
                )
                terminal_tree_mode_annihilator_checks += mode_annihilator_count
                terminal_tree_productive_mode_annihilator_checks += (
                    productive_mode_annihilator_count
                )
                audit_branch_vertices += branch_count
                audit_branch_pairs += branch_pair_count
                audit_productive_branch_pairs += productive_branch_pair_count
                audit_mode_packets += mode_packet_count
                audit_productive_mode_packets += productive_mode_packet_count
                audit_mode_rank_checks += mode_rank_count
                audit_productive_mode_rank_checks += productive_mode_rank_count
                audit_mode_peeling_checks += mode_peeling_count
                audit_productive_mode_peeling_checks += productive_mode_peeling_count
                audit_mode_annihilator_checks += mode_annihilator_count
                audit_productive_mode_annihilator_checks += (
                    productive_mode_annihilator_count
                )
                if tree_count > 1:
                    terminal_tree_multiflag_cores += 1
                    audit_multiflag_cores += 1
                if tree_count != terminal_paths_by_core[core]:
                    tree_recursion_defects += 1
                    case_filtration_path_defect += 1
                    raise AssertionError(
                        {
                            "kind": "terminal-tree-recursion-count-failed",
                            "p": p,
                            "k": k,
                            "syndrome": list(syn),
                            "fixed_roots": list(fixed_roots),
                            "core": list(core),
                            "tree_count": tree_count,
                            "enumerated_terminal_paths": (
                                terminal_paths_by_core[core]
                            ),
                        }
                    )
                if tree_count > 1 and productive_branch_pair_count == 0:
                    tree_recursion_defects += 1
                    case_filtration_path_defect += 1
                    raise AssertionError(
                        {
                            "kind": (
                                "terminal-multiflag-without-"
                                "productive-branch-pair"
                            ),
                            "p": p,
                            "k": k,
                            "syndrome": list(syn),
                            "fixed_roots": list(fixed_roots),
                            "core": list(core),
                            "terminal_paths": tree_count,
                            "branch_pairs": branch_pair_count,
                        }
                    )
                if any(syn):
                    max_nonzero_terminal_tree_count = max(
                        max_nonzero_terminal_tree_count,
                        tree_count,
                    )
                    max_nonzero_terminal_tree_branch_vertices = max(
                        max_nonzero_terminal_tree_branch_vertices,
                        branch_count,
                    )
                    max_nonzero_terminal_tree_branch_pairs = max(
                        max_nonzero_terminal_tree_branch_pairs,
                        branch_pair_count,
                    )
                    max_nonzero_terminal_tree_productive_branch_pairs = max(
                        max_nonzero_terminal_tree_productive_branch_pairs,
                        productive_branch_pair_count,
                    )
                    max_nonzero_terminal_tree_mode_packets = max(
                        max_nonzero_terminal_tree_mode_packets,
                        mode_packet_count,
                    )
                    max_nonzero_terminal_tree_productive_mode_packets = max(
                        max_nonzero_terminal_tree_productive_mode_packets,
                        productive_mode_packet_count,
                    )
                    max_nonzero_terminal_tree_mode_size = max(
                        max_nonzero_terminal_tree_mode_size,
                        max_mode_size,
                    )
                    max_nonzero_terminal_tree_mode_rank_checks = max(
                        max_nonzero_terminal_tree_mode_rank_checks,
                        mode_rank_count,
                    )
                    max_nonzero_terminal_tree_mode_rank_size = max(
                        max_nonzero_terminal_tree_mode_rank_size,
                        max_mode_rank_size,
                    )
                    max_nonzero_terminal_tree_mode_peeling_checks = max(
                        max_nonzero_terminal_tree_mode_peeling_checks,
                        mode_peeling_count,
                    )
                    max_nonzero_terminal_tree_mode_annihilator_checks = max(
                        max_nonzero_terminal_tree_mode_annihilator_checks,
                        mode_annihilator_count,
                    )
            visible_packet_total = sum(visible_packet_productions.values())
            if visible_packet_total != audit_mode_packets:
                raise AssertionError(
                    {
                        "kind": "visible-packet-production-count-mismatch",
                        "p": p,
                        "k": k,
                        "syndrome": list(syn),
                        "fixed_roots": list(fixed_roots),
                        "visible_packet_total": visible_packet_total,
                        "mode_packets": audit_mode_packets,
                    }
                )
            productive_visible_packet_total = sum(
                productive_visible_packet_productions.values()
            )
            if productive_visible_packet_total != audit_productive_mode_packets:
                raise AssertionError(
                    {
                        "kind": (
                            "productive-visible-packet-production-"
                            "count-mismatch"
                        ),
                        "p": p,
                        "k": k,
                        "syndrome": list(syn),
                        "fixed_roots": list(fixed_roots),
                        "productive_visible_packet_total": (
                            productive_visible_packet_total
                        ),
                        "productive_mode_packets": (
                            audit_productive_mode_packets
                        ),
                    }
                )

            def audit_anchor_base_kernel_relations(
                anchor_bases_by_label: dict[
                    tuple[int, tuple[tuple[int, int], ...]],
                    list[tuple[int, ...]],
                ],
                productive: bool,
            ) -> int:
                kernel_checks = 0
                for label, anchor_bases in anchor_bases_by_label.items():
                    mode_count = label[0]
                    row_count = t + mode_count
                    for left_base, right_base in itertools.combinations(
                        sorted(set(anchor_bases)),
                        2,
                    ):
                        if len(left_base) != len(right_base):
                            raise AssertionError(
                                {
                                    "kind": (
                                        "productive-"
                                        if productive
                                        else ""
                                    )
                                    + "visible-packet-anchor-base-"
                                    "degree-mismatch",
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "fixed_roots": list(fixed_roots),
                                    "mode_count": mode_count,
                                    "left_anchor_base": list(left_base),
                                    "right_anchor_base": list(right_base),
                                }
                            )
                        left_locator = cached_locator(left_base)
                        right_locator = cached_locator(right_base)
                        locator_difference = tuple(
                            (left - right) % p
                            for left, right in zip(
                                left_locator,
                                right_locator,
                            )
                        )
                        if locator_difference[-1] != 0:
                            raise AssertionError(
                                {
                                    "kind": (
                                        "productive-"
                                        if productive
                                        else ""
                                    )
                                    + "visible-packet-anchor-base-"
                                    "leading-term-not-cancelled",
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "fixed_roots": list(fixed_roots),
                                    "mode_count": mode_count,
                                    "left_anchor_base": list(left_base),
                                    "right_anchor_base": list(right_base),
                                    "locator_difference": list(
                                        locator_difference
                                    ),
                                }
                            )
                        lower_difference = locator_difference[:-1]
                        kernel_image = hankel_apply(
                            syn,
                            lower_difference,
                            row_count,
                            p,
                        )
                        if any(kernel_image):
                            raise AssertionError(
                                {
                                    "kind": (
                                        "productive-"
                                        if productive
                                        else ""
                                    )
                                    + "visible-packet-anchor-base-"
                                    "kernel-drop-failed",
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "fixed_roots": list(fixed_roots),
                                    "mode_count": mode_count,
                                    "left_anchor_base": list(left_base),
                                    "right_anchor_base": list(right_base),
                                    "lower_difference": list(
                                        lower_difference
                                    ),
                                    "kernel_image": list(kernel_image),
                                }
                            )
                        kernel_checks += 1
                return kernel_checks

            anchor_base_kernel_checks = audit_anchor_base_kernel_relations(
                visible_packet_anchor_bases,
                productive=False,
            )
            productive_anchor_base_kernel_checks = (
                audit_anchor_base_kernel_relations(
                    productive_visible_packet_anchor_bases,
                    productive=True,
                )
            )
            terminal_tree_anchor_base_kernel_checks += anchor_base_kernel_checks
            terminal_tree_productive_anchor_base_kernel_checks += (
                productive_anchor_base_kernel_checks
            )

            def audit_total_split_support_fibers(
                fibers: dict[
                    tuple[int, tuple[int, ...]],
                    list[tuple[int, ...]],
                ],
                productive: bool,
            ) -> tuple[int, int, int, int, int]:
                fiber_checks = 0
                fiber_labels = 0
                max_fiber_size = 0
                factorization_checks = 0
                max_marked_roots = 0
                for (mode_count, total_support), mode_supports in fibers.items():
                    marked_roots = marked_roots_for_split_support(
                        total_support
                    )
                    marked_root_indices = sorted(marked_roots)
                    marked_root_set = set(marked_root_indices)
                    max_marked_roots = max(
                        max_marked_roots,
                        len(marked_root_indices),
                    )
                    unique_supports = sorted(set(mode_supports))
                    fiber_size = len(unique_supports)
                    capacity = math.comb(
                        len(marked_root_indices),
                        mode_count,
                    )
                    fiber_checks += 1
                    fiber_labels += fiber_size
                    max_fiber_size = max(max_fiber_size, fiber_size)
                    if fiber_size > capacity:
                        raise AssertionError(
                            {
                                "kind": (
                                    "productive-"
                                    if productive
                                    else ""
                                )
                                + "total-split-support-fiber-"
                                "capacity-failed",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "total_split_support": list(total_support),
                                "mode_count": mode_count,
                                "fiber_size": fiber_size,
                                "marked_roots": marked_root_indices,
                                "capacity": capacity,
                            }
                        )
                    for support in unique_supports:
                        if not set(support) <= marked_root_set:
                            raise AssertionError(
                                {
                                    "kind": (
                                        "productive-"
                                        if productive
                                        else ""
                                    )
                                    + "total-split-support-fiber-"
                                    "unmarked-mode",
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "fixed_roots": list(fixed_roots),
                                    "total_split_support": list(
                                        total_support
                                    ),
                                    "mode_count": mode_count,
                                    "support": list(support),
                                    "marked_roots": marked_root_indices,
                                }
                            )
                    for candidate_modes in itertools.combinations(
                        marked_root_indices,
                        mode_count,
                    ):
                        candidate_anchor, expected = marked_subset_packet(
                            total_support,
                            candidate_modes,
                            marked_roots,
                        )
                        anchor_vector = hankel_apply(
                            syn,
                            cached_locator(candidate_anchor),
                            t + mode_count,
                            p,
                        )
                        if anchor_vector != tuple(expected):
                            raise AssertionError(
                                {
                                    "kind": (
                                        "productive-"
                                        if productive
                                        else ""
                                    )
                                    + "total-split-support-factorization-"
                                    "failed",
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "fixed_roots": list(fixed_roots),
                                    "total_split_support": list(
                                        total_support
                                    ),
                                    "mode_count": mode_count,
                                    "candidate_modes": list(
                                        candidate_modes
                                    ),
                                    "candidate_anchor": list(
                                        candidate_anchor
                                    ),
                                    "anchor_vector": list(anchor_vector),
                                    "expected": expected,
                                }
                            )
                        factorization_checks += 1
                return (
                    fiber_checks,
                    fiber_labels,
                    max_fiber_size,
                    factorization_checks,
                    max_marked_roots,
                )

            (
                total_split_support_fiber_checks,
                total_split_support_fiber_labels,
                total_split_support_fiber_max_size,
                total_split_support_factorization_checks,
                total_split_support_max_marked_roots,
            ) = audit_total_split_support_fibers(
                total_split_support_fibers,
                productive=False,
            )
            (
                productive_total_split_support_fiber_checks,
                productive_total_split_support_fiber_labels,
                productive_total_split_support_fiber_max_size,
                productive_total_split_support_factorization_checks,
                productive_total_split_support_max_marked_roots,
            ) = audit_total_split_support_fibers(
                productive_total_split_support_fibers,
                productive=True,
            )
            terminal_tree_total_split_support_fiber_checks += (
                total_split_support_fiber_checks
            )
            terminal_tree_productive_total_split_support_fiber_checks += (
                productive_total_split_support_fiber_checks
            )
            terminal_tree_total_split_support_fiber_labels += (
                total_split_support_fiber_labels
            )
            terminal_tree_productive_total_split_support_fiber_labels += (
                productive_total_split_support_fiber_labels
            )
            terminal_tree_total_split_support_fiber_max_size = max(
                terminal_tree_total_split_support_fiber_max_size,
                total_split_support_fiber_max_size,
            )
            terminal_tree_productive_total_split_support_fiber_max_size = max(
                terminal_tree_productive_total_split_support_fiber_max_size,
                productive_total_split_support_fiber_max_size,
            )
            terminal_tree_total_split_support_factorization_checks += (
                total_split_support_factorization_checks
            )
            terminal_tree_productive_total_split_support_factorization_checks += (
                productive_total_split_support_factorization_checks
            )
            terminal_tree_total_split_support_max_marked_roots = max(
                terminal_tree_total_split_support_max_marked_roots,
                total_split_support_max_marked_roots,
            )
            terminal_tree_productive_total_split_support_max_marked_roots = max(
                terminal_tree_productive_total_split_support_max_marked_roots,
                productive_total_split_support_max_marked_roots,
            )

            def audit_marked_exit_cubes(
                supports: set[tuple[int, ...]],
                productive: bool,
            ) -> tuple[int, int, int, int]:
                support_checks = 0
                face_checks = 0
                ordered_flags = 0
                max_marked_roots = 0
                for total_support in sorted(supports):
                    marked_roots = marked_roots_for_split_support(
                        total_support
                    )
                    marked_root_indices = sorted(marked_roots)
                    marked_count = len(marked_root_indices)
                    support_checks += 1
                    max_marked_roots = max(max_marked_roots, marked_count)
                    ordered_flags += math.factorial(marked_count)
                    for mode_count in range(1, marked_count + 1):
                        for candidate_modes in itertools.combinations(
                            marked_root_indices,
                            mode_count,
                        ):
                            candidate_anchor, expected = marked_subset_packet(
                                total_support,
                                candidate_modes,
                                marked_roots,
                            )
                            anchor_vector = hankel_apply(
                                syn,
                                cached_locator(candidate_anchor),
                                t + mode_count,
                                p,
                            )
                            if anchor_vector != tuple(expected):
                                raise AssertionError(
                                    {
                                        "kind": (
                                            "productive-"
                                            if productive
                                            else ""
                                        )
                                        + "marked-exit-cube-face-"
                                        "failed",
                                        "p": p,
                                        "k": k,
                                        "syndrome": list(syn),
                                        "fixed_roots": list(fixed_roots),
                                        "total_split_support": list(
                                            total_support
                                        ),
                                        "candidate_modes": list(
                                            candidate_modes
                                        ),
                                        "candidate_anchor": list(
                                            candidate_anchor
                                        ),
                                        "anchor_vector": list(
                                            anchor_vector
                                        ),
                                        "expected": expected,
                                    }
                                )
                            if not any(anchor_vector):
                                raise AssertionError(
                                    {
                                        "kind": (
                                            "productive-"
                                            if productive
                                            else ""
                                        )
                                        + "marked-exit-cube-face-zero",
                                        "p": p,
                                        "k": k,
                                        "syndrome": list(syn),
                                        "fixed_roots": list(fixed_roots),
                                        "total_split_support": list(
                                            total_support
                                        ),
                                        "candidate_modes": list(
                                            candidate_modes
                                        ),
                                        "candidate_anchor": list(
                                            candidate_anchor
                                        ),
                                    }
                                )
                            face_checks += 1
                return (
                    support_checks,
                    face_checks,
                    ordered_flags,
                    max_marked_roots,
                )

            (
                marked_exit_cube_support_checks,
                marked_exit_cube_face_checks,
                marked_exit_cube_ordered_flags,
                marked_exit_cube_max_marked_roots,
            ) = audit_marked_exit_cubes(
                total_split_supports,
                productive=False,
            )
            (
                productive_marked_exit_cube_support_checks,
                productive_marked_exit_cube_face_checks,
                productive_marked_exit_cube_ordered_flags,
                productive_marked_exit_cube_max_marked_roots,
            ) = audit_marked_exit_cubes(
                productive_total_split_supports,
                productive=True,
            )
            terminal_tree_marked_exit_cube_support_checks += (
                marked_exit_cube_support_checks
            )
            terminal_tree_productive_marked_exit_cube_support_checks += (
                productive_marked_exit_cube_support_checks
            )
            terminal_tree_marked_exit_cube_face_checks += (
                marked_exit_cube_face_checks
            )
            terminal_tree_productive_marked_exit_cube_face_checks += (
                productive_marked_exit_cube_face_checks
            )
            terminal_tree_marked_exit_cube_ordered_flags += (
                marked_exit_cube_ordered_flags
            )
            terminal_tree_productive_marked_exit_cube_ordered_flags += (
                productive_marked_exit_cube_ordered_flags
            )
            terminal_tree_marked_exit_cube_max_marked_roots = max(
                terminal_tree_marked_exit_cube_max_marked_roots,
                marked_exit_cube_max_marked_roots,
            )
            terminal_tree_productive_marked_exit_cube_max_marked_roots = max(
                terminal_tree_productive_marked_exit_cube_max_marked_roots,
                productive_marked_exit_cube_max_marked_roots,
            )

            def audit_marked_core_fibers(
                supports: set[tuple[int, ...]],
                productive: bool,
            ) -> tuple[
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
                int,
            ]:
                fibers: dict[
                    tuple[int, tuple[int, ...]],
                    list[tuple[int, ...]],
                ] = {}
                for total_support in supports:
                    marked_roots = marked_roots_for_split_support(
                        total_support
                    )
                    marked_support = tuple(sorted(marked_roots))
                    if not marked_support:
                        continue
                    marked_set = set(marked_support)
                    unmarked_core = tuple(
                        index
                        for index in total_support
                        if index not in marked_set
                    )
                    fibers.setdefault(
                        (len(marked_support), unmarked_core),
                        [],
                    ).append(marked_support)

                fiber_checks = 0
                fiber_labels = 0
                max_fiber_size = 0
                nonempty_boundary_checks = 0
                nonempty_boundary_max_size = 0
                empty_boundary_checks = 0
                empty_boundary_labels = 0
                empty_boundary_max_size = 0
                empty_boundary_root_linear_checks = 0
                empty_boundary_root_linear_hits = 0
                empty_boundary_complement_pair_checks = 0
                moment_complete_checks = 0
                moment_complete_max_size = 0
                deficit_packing_checks = 0
                deficit_packing_max_deficit = 0
                deficit_packing_max_size = 0
                deficit_anchor_label_checks = 0
                deficit_anchor_max_labels = 0
                deficit_anchor_kernel_checks = 0
                deficit_anchor_max_residual_size = 0
                deficit_anchor_residual_fiber_checks = 0
                deficit_anchor_residual_fiber_labels = 0
                deficit_anchor_residual_fiber_max_size = 0
                deficit_anchor_residual_fiber_max_direction = 0
                deficit_anchor_line_kernel_checks = 0
                deficit_anchor_line_kernel_max_direction_roots = 0
                deficit_anchor_line_kernel_max_sharp_bound = 0
                deficit_anchor_direction_mds_checks = 0
                deficit_anchor_direction_mds_bad_subsets = 0
                deficit_anchor_direction_mds_max_bad_subsets = 0
                deficit_anchor_direction_mds_max_bound = 0
                deficit_anchor_root_slice_checks = 0
                deficit_anchor_root_slice_labels = 0
                deficit_anchor_root_slice_bad_labels = 0
                deficit_anchor_root_slice_max_bad_per_anchor = 0
                deficit_anchor_endpoint_rank_checks = 0
                deficit_anchor_endpoint_rank_defects = 0
                deficit_anchor_endpoint_rank_max_defect = 0
                for (marked_count, unmarked_core), supports_in_fiber in (
                    fibers.items()
                ):
                    unique_supports = sorted(set(supports_in_fiber))
                    fiber_size = len(unique_supports)
                    fiber_checks += 1
                    fiber_labels += fiber_size
                    max_fiber_size = max(max_fiber_size, fiber_size)
                    moment_deficit = max(0, marked_count - t)
                    if len(unmarked_core) >= moment_deficit:
                        moment_complete_checks += 1
                        moment_complete_max_size = max(
                            moment_complete_max_size,
                            fiber_size,
                        )
                        if fiber_size > 1:
                            raise AssertionError(
                                {
                                    "kind": (
                                        "productive-"
                                        if productive
                                        else ""
                                    )
                                    + "marked-core-moment-complete-"
                                    "uniqueness-failed",
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "fixed_roots": list(fixed_roots),
                                    "unmarked_core": list(unmarked_core),
                                    "marked_count": marked_count,
                                    "moment_deficit": moment_deficit,
                                    "supports": [
                                        list(support)
                                        for support in unique_supports
                                    ],
                                }
                            )
                    core_deficit = (
                        marked_count
                        - t
                        - len(unmarked_core)
                    )
                    if core_deficit > 0:
                        deficit_packing_checks += 1
                        deficit_packing_max_deficit = max(
                            deficit_packing_max_deficit,
                            core_deficit,
                        )
                        deficit_packing_max_size = max(
                            deficit_packing_max_size,
                            fiber_size,
                        )
                        support_sets = [
                            set(support) for support in unique_supports
                        ]
                        for left_index, right_index in itertools.combinations(
                            range(len(unique_supports)),
                            2,
                        ):
                            overlap = len(
                                support_sets[left_index]
                                & support_sets[right_index]
                            )
                            if overlap >= core_deficit:
                                raise AssertionError(
                                    {
                                        "kind": (
                                            "productive-"
                                            if productive
                                            else ""
                                        )
                                        + "marked-core-deficit-packing-"
                                        "overlap-failed",
                                        "p": p,
                                        "k": k,
                                        "syndrome": list(syn),
                                        "fixed_roots": list(fixed_roots),
                                        "unmarked_core": list(
                                            unmarked_core
                                        ),
                                        "marked_count": marked_count,
                                        "core_deficit": core_deficit,
                                        "left_support": list(
                                            unique_supports[left_index]
                                        ),
                                        "right_support": list(
                                            unique_supports[right_index]
                                        ),
                                        "overlap": overlap,
                                    }
                                )
                        packed_subsets = fiber_size * math.comb(
                            marked_count,
                            core_deficit,
                        )
                        deficit_anchor_label_checks += packed_subsets
                        deficit_anchor_max_labels = max(
                            deficit_anchor_max_labels,
                            packed_subsets,
                        )
                        anchor_to_support: dict[
                            tuple[int, ...],
                            tuple[int, ...],
                        ] = {}
                        for support in unique_supports:
                            for anchor in itertools.combinations(
                                support,
                                core_deficit,
                            ):
                                previous = anchor_to_support.get(anchor)
                                if (
                                    previous is not None
                                    and previous != support
                                ):
                                    raise AssertionError(
                                        {
                                            "kind": (
                                                "productive-"
                                                if productive
                                                else ""
                                            )
                                            + "marked-core-deficit-anchor-"
                                            "injection-failed",
                                            "p": p,
                                            "k": k,
                                            "syndrome": list(syn),
                                            "fixed_roots": list(
                                                fixed_roots
                                            ),
                                            "unmarked_core": list(
                                                unmarked_core
                                            ),
                                            "marked_count": marked_count,
                                            "core_deficit": core_deficit,
                                            "anchor": list(anchor),
                                            "left_support": list(previous),
                                            "right_support": list(support),
                                        }
                                    )
                                anchor_to_support[anchor] = support
                                residual_support = tuple(
                                    root
                                    for root in support
                                    if root not in anchor
                                )
                                residual_size = len(residual_support)
                                if residual_size != (
                                    marked_count - core_deficit
                                ):
                                    raise AssertionError(
                                        {
                                            "kind": (
                                                "productive-"
                                                if productive
                                                else ""
                                            )
                                            + "marked-core-deficit-anchor-"
                                            "residual-size-failed",
                                            "p": p,
                                            "k": k,
                                            "syndrome": list(syn),
                                            "fixed_roots": list(
                                                fixed_roots
                                            ),
                                            "unmarked_core": list(
                                                unmarked_core
                                            ),
                                            "marked_count": marked_count,
                                            "core_deficit": core_deficit,
                                            "anchor": list(anchor),
                                            "residual_support": list(
                                                residual_support
                                            ),
                                        }
                                    )
                                anchor_locator = cached_locator(anchor)
                                filtered_sequence = hankel_apply(
                                    syn,
                                    anchor_locator,
                                    2 * residual_size,
                                    p,
                                )
                                deficit_anchor_kernel_checks += 1
                                deficit_anchor_max_residual_size = max(
                                    deficit_anchor_max_residual_size,
                                    residual_size,
                                )
                                if residual_size:
                                    residual_locator = cached_locator(
                                        residual_support
                                    )
                                    if not hankel_annihilates(
                                        filtered_sequence,
                                        residual_locator,
                                        residual_size,
                                        p,
                                    ):
                                        raise AssertionError(
                                            {
                                                "kind": (
                                                    "productive-"
                                                    if productive
                                                    else ""
                                                )
                                                + "marked-core-deficit-"
                                                "anchor-kernel-failed",
                                                "p": p,
                                                "k": k,
                                                "syndrome": list(syn),
                                                "fixed_roots": list(
                                                    fixed_roots
                                                ),
                                                "unmarked_core": list(
                                                    unmarked_core
                                                ),
                                                "marked_count": marked_count,
                                                "core_deficit": core_deficit,
                                                "anchor": list(anchor),
                                                "residual_support": list(
                                                    residual_support
                                                ),
                                                "filtered_sequence": list(
                                                    filtered_sequence
                                                ),
                                                "residual_locator": list(
                                                    residual_locator
                                                ),
                                            }
                                        )
                                    moment_matrix = tuple(
                                        tuple(
                                            filtered_sequence[row + column]
                                            for column in range(
                                                residual_size
                                            )
                                        )
                                        for row in range(residual_size)
                                    )
                                    rhs = tuple(
                                        (
                                            -filtered_sequence[
                                                row + residual_size
                                            ]
                                        )
                                        % p
                                        for row in range(residual_size)
                                    )
                                    recovered_locator = (
                                        solve_square_mod(
                                            moment_matrix,
                                            rhs,
                                            p,
                                        )
                                        + (1,)
                                    )
                                    if recovered_locator != residual_locator:
                                        raise AssertionError(
                                            {
                                                "kind": (
                                                    "productive-"
                                                    if productive
                                                    else ""
                                                )
                                                + "marked-core-deficit-"
                                                "anchor-recovery-failed",
                                                "p": p,
                                                "k": k,
                                                "syndrome": list(syn),
                                                "fixed_roots": list(
                                                    fixed_roots
                                                ),
                                                "unmarked_core": list(
                                                    unmarked_core
                                                ),
                                                "marked_count": marked_count,
                                                "core_deficit": core_deficit,
                                                "anchor": list(anchor),
                                                "residual_support": list(
                                                    residual_support
                                                ),
                                                "recovered_locator": list(
                                                    recovered_locator
                                                ),
                                                "residual_locator": list(
                                                    residual_locator
                                                ),
                                            }
                                        )
                                    available_roots = tuple(
                                        root
                                        for root in range(n)
                                        if root not in set(unmarked_core)
                                        and root not in set(anchor)
                                    )
                                    residual_candidates = []
                                    for candidate in itertools.combinations(
                                        available_roots,
                                        residual_size,
                                    ):
                                        candidate_locator = cached_locator(
                                            candidate
                                        )
                                        filtered_candidate_vector = hankel_apply(
                                            filtered_sequence,
                                            candidate_locator,
                                            residual_size,
                                            p,
                                        )
                                        product_locator = multiply_polynomials_mod(
                                            anchor_locator,
                                            candidate_locator,
                                            p,
                                        )
                                        divisible_candidate_vector = hankel_apply(
                                            syn,
                                            product_locator,
                                            residual_size,
                                            p,
                                        )
                                        if (
                                            filtered_candidate_vector
                                            != divisible_candidate_vector
                                        ):
                                            raise AssertionError(
                                                {
                                                    "kind": (
                                                        "productive-"
                                                        if productive
                                                        else ""
                                                    )
                                                    + "marked-core-deficit-"
                                                    "anchor-divisible-kernel-"
                                                    "failed",
                                                    "p": p,
                                                    "k": k,
                                                    "syndrome": list(syn),
                                                    "fixed_roots": list(
                                                        fixed_roots
                                                    ),
                                                    "unmarked_core": list(
                                                        unmarked_core
                                                    ),
                                                    "marked_count": marked_count,
                                                    "core_deficit": core_deficit,
                                                    "anchor": list(anchor),
                                                    "candidate": list(candidate),
                                                    "filtered_vector": list(
                                                        filtered_candidate_vector
                                                    ),
                                                    "divisible_vector": list(
                                                        divisible_candidate_vector
                                                    ),
                                                    "anchor_locator": list(
                                                        anchor_locator
                                                    ),
                                                    "candidate_locator": list(
                                                        candidate_locator
                                                    ),
                                                    "product_locator": list(
                                                        product_locator
                                                    ),
                                                }
                                            )
                                        if not any(filtered_candidate_vector):
                                            residual_candidates.append(
                                                candidate
                                            )
                                    if (
                                        residual_support
                                        not in residual_candidates
                                    ):
                                        raise AssertionError(
                                            {
                                                "kind": (
                                                    "productive-"
                                                    if productive
                                                    else ""
                                                )
                                                + "marked-core-deficit-"
                                                "anchor-residual-missing",
                                                "p": p,
                                                "k": k,
                                                "syndrome": list(syn),
                                                "fixed_roots": list(
                                                    fixed_roots
                                                ),
                                                "unmarked_core": list(
                                                    unmarked_core
                                                ),
                                                "marked_count": marked_count,
                                                "core_deficit": core_deficit,
                                                "anchor": list(anchor),
                                                "residual_support": list(
                                                    residual_support
                                                ),
                                                "candidates": [
                                                    list(candidate)
                                                    for candidate in (
                                                        residual_candidates
                                                    )
                                                ],
                                            }
                                        )
                                    root_slice_bad_roots: set[int] = set()
                                    endpoint_defect = 0
                                    root_slice_persistent = False
                                    if residual_size > 1:
                                        root_slice_width = residual_size - 1
                                        endpoint_columns = tuple(
                                            hankel_apply(
                                                syn,
                                                shift_locator(
                                                    anchor_locator,
                                                    column,
                                                ),
                                                residual_size,
                                                p,
                                            )
                                            for column in range(
                                                root_slice_width
                                            )
                                        )
                                        endpoint_matrix = tuple(
                                            tuple(
                                                endpoint_columns[column][row]
                                                for column in range(
                                                    root_slice_width
                                                )
                                            )
                                            for row in range(residual_size)
                                        )
                                        endpoint_from_filtered = tuple(
                                            tuple(
                                                filtered_sequence[row + column]
                                                for column in range(
                                                    root_slice_width
                                                )
                                            )
                                            for row in range(residual_size)
                                        )
                                        if (
                                            endpoint_matrix
                                            != endpoint_from_filtered
                                        ):
                                            raise AssertionError(
                                                {
                                                    "kind": (
                                                        "productive-"
                                                        if productive
                                                        else ""
                                                    )
                                                    + "marked-core-deficit-"
                                                    "anchor-endpoint-prefix-"
                                                    "identity-failed",
                                                    "p": p,
                                                    "k": k,
                                                    "syndrome": list(syn),
                                                    "fixed_roots": list(
                                                        fixed_roots
                                                    ),
                                                    "unmarked_core": list(
                                                        unmarked_core
                                                    ),
                                                    "marked_count": marked_count,
                                                    "core_deficit": core_deficit,
                                                    "anchor": list(anchor),
                                                    "endpoint_matrix": [
                                                        list(row)
                                                        for row in (
                                                            endpoint_matrix
                                                        )
                                                    ],
                                                    "endpoint_from_filtered": [
                                                        list(row)
                                                        for row in (
                                                            endpoint_from_filtered
                                                        )
                                                    ],
                                                }
                                            )
                                        endpoint_rank = matrix_rank_mod(
                                            endpoint_matrix,
                                            p,
                                        )
                                        endpoint_defect = (
                                            root_slice_width - endpoint_rank
                                        )
                                        deficit_anchor_endpoint_rank_checks += 1
                                        if endpoint_defect:
                                            deficit_anchor_endpoint_rank_defects += 1
                                        deficit_anchor_endpoint_rank_max_defect = max(
                                            deficit_anchor_endpoint_rank_max_defect,
                                            endpoint_defect,
                                        )
                                        deficit_anchor_root_slice_checks += 1
                                        deficit_anchor_root_slice_labels += (
                                            len(available_roots)
                                        )
                                        for root in available_roots:
                                            root_divisor_locator = (
                                                multiply_polynomials_mod(
                                                    anchor_locator,
                                                    cached_locator((root,)),
                                                    p,
                                                )
                                            )
                                            root_slice_columns = tuple(
                                                hankel_apply(
                                                    syn,
                                                    shift_locator(
                                                        root_divisor_locator,
                                                        column,
                                                    ),
                                                    residual_size,
                                                    p,
                                                )
                                                for column in range(
                                                    root_slice_width
                                                )
                                            )
                                            root_slice_matrix = tuple(
                                                tuple(
                                                    root_slice_columns[column][
                                                        row
                                                    ]
                                                    for column in range(
                                                        root_slice_width
                                                    )
                                                )
                                                for row in range(residual_size)
                                            )
                                            absorbed_sequence = hankel_apply(
                                                syn,
                                                root_divisor_locator,
                                                2 * residual_size - 2,
                                                p,
                                            )
                                            absorbed_root_slice_matrix = tuple(
                                                tuple(
                                                    absorbed_sequence[
                                                        row + column
                                                    ]
                                                    for column in range(
                                                        root_slice_width
                                                    )
                                                )
                                                for row in range(residual_size)
                                            )
                                            if (
                                                root_slice_matrix
                                                != absorbed_root_slice_matrix
                                            ):
                                                raise AssertionError(
                                                    {
                                                        "kind": (
                                                            "productive-"
                                                            if productive
                                                            else ""
                                                        )
                                                        + "marked-core-"
                                                        "deficit-anchor-"
                                                        "absorbed-root-slice-"
                                                        "identity-failed",
                                                        "p": p,
                                                        "k": k,
                                                        "syndrome": list(syn),
                                                        "fixed_roots": list(
                                                            fixed_roots
                                                        ),
                                                        "unmarked_core": list(
                                                            unmarked_core
                                                        ),
                                                        "marked_count": (
                                                            marked_count
                                                        ),
                                                        "core_deficit": (
                                                            core_deficit
                                                        ),
                                                        "anchor": list(anchor),
                                                        "root": root,
                                                        "root_slice_matrix": [
                                                            list(row)
                                                            for row in (
                                                                root_slice_matrix
                                                            )
                                                        ],
                                                        "absorbed_matrix": [
                                                            list(row)
                                                            for row in (
                                                                absorbed_root_slice_matrix
                                                            )
                                                        ],
                                                    }
                                                )
                                            root_slice_rank = matrix_rank_mod(
                                                root_slice_matrix,
                                                p,
                                            )
                                            if root_slice_rank < root_slice_width:
                                                root_slice_bad_roots.add(root)
                                        deficit_anchor_root_slice_bad_labels += (
                                            len(root_slice_bad_roots)
                                        )
                                        deficit_anchor_root_slice_max_bad_per_anchor = max(
                                            deficit_anchor_root_slice_max_bad_per_anchor,
                                            len(root_slice_bad_roots),
                                        )
                                        root_slice_persistent = True
                                        for probe_root in range(p):
                                            probe_matrix = tuple(
                                                tuple(
                                                    (
                                                        filtered_sequence[
                                                            row + column + 1
                                                        ]
                                                        - probe_root
                                                        * filtered_sequence[
                                                            row + column
                                                        ]
                                                    )
                                                    % p
                                                    for column in range(
                                                        root_slice_width
                                                    )
                                                )
                                                for row in range(residual_size)
                                            )
                                            if (
                                                matrix_rank_mod(
                                                    probe_matrix,
                                                    p,
                                                )
                                                == root_slice_width
                                            ):
                                                root_slice_persistent = False
                                                break
                                        if (
                                            not root_slice_persistent
                                            and len(root_slice_bad_roots)
                                            > root_slice_width
                                        ):
                                            raise AssertionError(
                                                {
                                                    "kind": (
                                                        "productive-"
                                                        if productive
                                                        else ""
                                                    )
                                                    + "marked-core-deficit-"
                                                    "anchor-root-slice-"
                                                    "finite-bound-failed",
                                                    "p": p,
                                                    "k": k,
                                                    "syndrome": list(syn),
                                                    "fixed_roots": list(
                                                        fixed_roots
                                                    ),
                                                    "unmarked_core": list(
                                                        unmarked_core
                                                    ),
                                                    "marked_count": marked_count,
                                                    "core_deficit": core_deficit,
                                                    "anchor": list(anchor),
                                                    "root_slice_bad_roots": (
                                                        sorted(
                                                            root_slice_bad_roots
                                                        )
                                                    ),
                                                    "bound": root_slice_width,
                                                }
                                            )
                                    for left, right in itertools.combinations(
                                        residual_candidates,
                                        2,
                                    ):
                                        shared_roots = set(left) & set(right)
                                        missing_roots = sorted(
                                            root
                                            for root in shared_roots
                                            if root not in root_slice_bad_roots
                                        )
                                        if missing_roots:
                                            raise AssertionError(
                                                {
                                                    "kind": (
                                                        "productive-"
                                                        if productive
                                                        else ""
                                                    )
                                                    + "marked-core-deficit-"
                                                    "anchor-root-slice-"
                                                    "collision-failed",
                                                    "p": p,
                                                    "k": k,
                                                    "syndrome": list(syn),
                                                    "fixed_roots": list(
                                                        fixed_roots
                                                    ),
                                                    "unmarked_core": list(
                                                        unmarked_core
                                                    ),
                                                    "marked_count": marked_count,
                                                    "core_deficit": core_deficit,
                                                    "anchor": list(anchor),
                                                    "left": list(left),
                                                    "right": list(right),
                                                    "missing_roots": (
                                                        missing_roots
                                                    ),
                                                    "root_slice_bad_roots": (
                                                        sorted(
                                                            root_slice_bad_roots
                                                        )
                                                    ),
                                                }
                                            )
                                    if residual_size > 1:
                                        absorbed_rank_bound = (
                                            (
                                                len(available_roots)
                                                - len(root_slice_bad_roots)
                                            )
                                            + len(root_slice_bad_roots)
                                            * math.comb(
                                                len(available_roots) - 1,
                                                residual_size - 1,
                                            )
                                        ) // residual_size
                                        if (
                                            len(residual_candidates)
                                            > absorbed_rank_bound
                                        ):
                                            raise AssertionError(
                                                {
                                                    "kind": (
                                                        "productive-"
                                                        if productive
                                                        else ""
                                                    )
                                                    + "marked-core-deficit-"
                                                    "anchor-absorbed-rank-"
                                                    "bound-failed",
                                                    "p": p,
                                                    "k": k,
                                                    "syndrome": list(syn),
                                                    "fixed_roots": list(
                                                        fixed_roots
                                                    ),
                                                    "unmarked_core": list(
                                                        unmarked_core
                                                    ),
                                                    "marked_count": marked_count,
                                                    "core_deficit": core_deficit,
                                                    "anchor": list(anchor),
                                                    "available_roots": list(
                                                        available_roots
                                                    ),
                                                    "root_slice_bad_roots": (
                                                        sorted(
                                                            root_slice_bad_roots
                                                        )
                                                    ),
                                                    "candidate_count": len(
                                                        residual_candidates
                                                    ),
                                                    "absorbed_rank_bound": (
                                                        absorbed_rank_bound
                                                    ),
                                                }
                                            )
                                    residual_direction_dim = (
                                        residual_size
                                        - matrix_rank_mod(
                                            moment_matrix,
                                            p,
                                        )
                                    )
                                    if (
                                        residual_size > 1
                                        and endpoint_defect
                                        > residual_direction_dim
                                    ):
                                        raise AssertionError(
                                            {
                                                "kind": (
                                                    "productive-"
                                                    if productive
                                                    else ""
                                                )
                                                + "marked-core-deficit-"
                                                "anchor-endpoint-direction-"
                                                "inclusion-failed",
                                                "p": p,
                                                "k": k,
                                                "syndrome": list(syn),
                                                "fixed_roots": list(
                                                    fixed_roots
                                                ),
                                                "unmarked_core": list(
                                                    unmarked_core
                                                ),
                                                "marked_count": marked_count,
                                                "core_deficit": core_deficit,
                                                "anchor": list(anchor),
                                                "endpoint_defect": (
                                                    endpoint_defect
                                                ),
                                                "residual_direction_dim": (
                                                    residual_direction_dim
                                                ),
                                            }
                                        )
                                    root_slice_persistence_certified = (
                                        residual_size > 1
                                        and root_slice_persistent
                                        and p >= residual_size
                                    )
                                    if (
                                        root_slice_persistence_certified
                                        and endpoint_defect == 0
                                    ):
                                        raise AssertionError(
                                            {
                                                "kind": (
                                                    "productive-"
                                                    if productive
                                                    else ""
                                                )
                                                + "marked-core-deficit-"
                                                "anchor-persistent-root-slice-"
                                                "endpoint-failed",
                                                "p": p,
                                                "k": k,
                                                "syndrome": list(syn),
                                                "fixed_roots": list(
                                                    fixed_roots
                                                ),
                                                "unmarked_core": list(
                                                    unmarked_core
                                                ),
                                                "marked_count": marked_count,
                                                "core_deficit": core_deficit,
                                                "anchor": list(anchor),
                                                "root_slice_bad_roots": sorted(
                                                    root_slice_bad_roots
                                                ),
                                                "endpoint_defect": (
                                                    endpoint_defect
                                                ),
                                            }
                                        )
                                    if (
                                        root_slice_persistence_certified
                                        and residual_direction_dim < 2
                                    ):
                                        raise AssertionError(
                                            {
                                                "kind": (
                                                    "productive-"
                                                    if productive
                                                    else ""
                                                )
                                                + "marked-core-deficit-"
                                                "anchor-persistent-root-slice-"
                                                "higher-direction-failed",
                                                "p": p,
                                                "k": k,
                                                "syndrome": list(syn),
                                                "fixed_roots": list(
                                                    fixed_roots
                                                ),
                                                "unmarked_core": list(
                                                    unmarked_core
                                                ),
                                                "marked_count": marked_count,
                                                "core_deficit": core_deficit,
                                                "anchor": list(anchor),
                                                "available_roots": list(
                                                    available_roots
                                                ),
                                                "root_slice_bad_roots": sorted(
                                                    root_slice_bad_roots
                                                ),
                                                "endpoint_defect": (
                                                    endpoint_defect
                                                ),
                                                "residual_direction_dim": (
                                                    residual_direction_dim
                                                ),
                                            }
                                        )
                                    if residual_direction_dim == 1:
                                        line_kernel_basis = right_kernel_basis_mod(
                                            moment_matrix,
                                            p,
                                        )
                                        if len(line_kernel_basis) != 1:
                                            raise AssertionError(
                                                {
                                                    "kind": (
                                                        "productive-"
                                                        if productive
                                                        else ""
                                                    )
                                                    + "marked-core-deficit-"
                                                    "anchor-line-kernel-basis-"
                                                    "failed",
                                                    "p": p,
                                                    "k": k,
                                                    "syndrome": list(syn),
                                                    "fixed_roots": list(
                                                        fixed_roots
                                                    ),
                                                    "unmarked_core": list(
                                                        unmarked_core
                                                    ),
                                                    "marked_count": marked_count,
                                                    "core_deficit": core_deficit,
                                                    "anchor": list(anchor),
                                                    "basis": [
                                                        list(vector)
                                                        for vector in (
                                                            line_kernel_basis
                                                        )
                                                    ],
                                                }
                                            )
                                        line_direction = line_kernel_basis[0]
                                        direction_roots = {
                                            root
                                            for root in available_roots
                                            if not polynomial_eval_mod(
                                                line_direction,
                                                domain[root],
                                                p,
                                            )
                                        }
                                        if (
                                            residual_size > 1
                                            and direction_roots
                                            != root_slice_bad_roots
                                        ):
                                            raise AssertionError(
                                                {
                                                    "kind": (
                                                        "productive-"
                                                        if productive
                                                        else ""
                                                    )
                                                    + "marked-core-deficit-"
                                                    "anchor-line-kernel-root-"
                                                    "slice-failed",
                                                    "p": p,
                                                    "k": k,
                                                    "syndrome": list(syn),
                                                    "fixed_roots": list(
                                                        fixed_roots
                                                    ),
                                                    "unmarked_core": list(
                                                        unmarked_core
                                                    ),
                                                    "marked_count": marked_count,
                                                    "core_deficit": core_deficit,
                                                    "anchor": list(anchor),
                                                    "line_direction": list(
                                                        line_direction
                                                    ),
                                                    "direction_roots": sorted(
                                                        direction_roots
                                                    ),
                                                    "root_slice_bad_roots": sorted(
                                                        root_slice_bad_roots
                                                    ),
                                                }
                                            )
                                        direction_root_count = len(
                                            direction_roots
                                        )
                                        line_kernel_bound = (
                                            len(available_roots)
                                            - direction_root_count
                                        ) // (
                                            residual_size
                                            - direction_root_count
                                        )
                                        deficit_anchor_line_kernel_checks += 1
                                        deficit_anchor_line_kernel_max_direction_roots = max(
                                            deficit_anchor_line_kernel_max_direction_roots,
                                            direction_root_count,
                                        )
                                        deficit_anchor_line_kernel_max_sharp_bound = max(
                                            deficit_anchor_line_kernel_max_sharp_bound,
                                            line_kernel_bound,
                                        )
                                        if (
                                            len(residual_candidates)
                                            > line_kernel_bound
                                        ):
                                            raise AssertionError(
                                                {
                                                    "kind": (
                                                        "productive-"
                                                        if productive
                                                        else ""
                                                    )
                                                    + "marked-core-deficit-"
                                                    "anchor-line-kernel-bound-"
                                                    "failed",
                                                    "p": p,
                                                    "k": k,
                                                    "syndrome": list(syn),
                                                    "fixed_roots": list(
                                                        fixed_roots
                                                    ),
                                                    "unmarked_core": list(
                                                        unmarked_core
                                                    ),
                                                    "marked_count": marked_count,
                                                    "core_deficit": core_deficit,
                                                    "anchor": list(anchor),
                                                    "line_direction": list(
                                                        line_direction
                                                    ),
                                                    "direction_roots": sorted(
                                                        direction_roots
                                                    ),
                                                    "candidate_count": len(
                                                        residual_candidates
                                                    ),
                                                    "bound": line_kernel_bound,
                                                }
                                            )
                                    if (
                                        0
                                        < residual_direction_dim
                                        < residual_size
                                    ):
                                        direction_basis = right_kernel_basis_mod(
                                            moment_matrix,
                                            p,
                                        )
                                        if (
                                            len(direction_basis)
                                            != residual_direction_dim
                                        ):
                                            raise AssertionError(
                                                {
                                                    "kind": (
                                                        "productive-"
                                                        if productive
                                                        else ""
                                                    )
                                                    + "marked-core-deficit-"
                                                    "anchor-direction-mds-"
                                                    "basis-failed",
                                                    "p": p,
                                                    "k": k,
                                                    "syndrome": list(syn),
                                                    "fixed_roots": list(
                                                        fixed_roots
                                                    ),
                                                    "unmarked_core": list(
                                                        unmarked_core
                                                    ),
                                                    "marked_count": marked_count,
                                                    "core_deficit": core_deficit,
                                                    "anchor": list(anchor),
                                                    "direction_dim": (
                                                        residual_direction_dim
                                                    ),
                                                    "basis": [
                                                        list(vector)
                                                        for vector in (
                                                            direction_basis
                                                        )
                                                    ],
                                                }
                                            )
                                        bad_direction_subsets: set[
                                            tuple[int, ...]
                                        ] = set()
                                        for subset in itertools.combinations(
                                            available_roots,
                                            residual_direction_dim,
                                        ):
                                            evaluation_matrix = tuple(
                                                tuple(
                                                    polynomial_eval_mod(
                                                        vector,
                                                        domain[root],
                                                        p,
                                                    )
                                                    for vector in (
                                                        direction_basis
                                                    )
                                                )
                                                for root in subset
                                            )
                                            if (
                                                matrix_rank_mod(
                                                    evaluation_matrix,
                                                    p,
                                                )
                                                < residual_direction_dim
                                            ):
                                                bad_direction_subsets.add(subset)
                                        projective_bad_subsets: set[
                                            tuple[int, ...]
                                        ] = set()
                                        for direction in (
                                            projective_span_representatives_mod(
                                                direction_basis,
                                                p,
                                            )
                                        ):
                                            direction_roots = tuple(
                                                root
                                                for root in available_roots
                                                if not polynomial_eval_mod(
                                                    direction,
                                                    domain[root],
                                                    p,
                                                )
                                            )
                                            for subset in itertools.combinations(
                                                direction_roots,
                                                residual_direction_dim,
                                            ):
                                                projective_bad_subsets.add(
                                                    subset
                                                )
                                        if (
                                            projective_bad_subsets
                                            != bad_direction_subsets
                                        ):
                                            raise AssertionError(
                                                {
                                                    "kind": (
                                                        "productive-"
                                                        if productive
                                                        else ""
                                                    )
                                                    + "marked-core-deficit-"
                                                    "anchor-direction-mds-"
                                                    "projective-shadow-failed",
                                                    "p": p,
                                                    "k": k,
                                                    "syndrome": list(syn),
                                                    "fixed_roots": list(
                                                        fixed_roots
                                                    ),
                                                    "unmarked_core": list(
                                                        unmarked_core
                                                    ),
                                                    "marked_count": marked_count,
                                                    "core_deficit": core_deficit,
                                                    "anchor": list(anchor),
                                                    "direction_dim": (
                                                        residual_direction_dim
                                                    ),
                                                    "bad_subsets": [
                                                        list(item)
                                                        for item in sorted(
                                                            bad_direction_subsets
                                                        )
                                                    ],
                                                    "projective_bad_subsets": [
                                                        list(item)
                                                        for item in sorted(
                                                            projective_bad_subsets
                                                        )
                                                    ],
                                                }
                                            )
                                        fixed_divisor_bad_subsets: set[
                                            tuple[int, ...]
                                        ] = set()
                                        fixed_divisor_width = (
                                            residual_size
                                            - residual_direction_dim
                                        )
                                        for subset in itertools.combinations(
                                            available_roots,
                                            residual_direction_dim,
                                        ):
                                            subset_divisor_locator = (
                                                multiply_polynomials_mod(
                                                    anchor_locator,
                                                    cached_locator(subset),
                                                    p,
                                                )
                                            )
                                            fixed_divisor_matrix = (
                                                hankel_divisor_matrix_mod(
                                                    syn,
                                                    subset_divisor_locator,
                                                    residual_size,
                                                    fixed_divisor_width,
                                                    p,
                                                )
                                            )
                                            if (
                                                matrix_rank_mod(
                                                    fixed_divisor_matrix,
                                                    p,
                                                )
                                                < fixed_divisor_width
                                            ):
                                                fixed_divisor_bad_subsets.add(
                                                    subset
                                                )
                                        if (
                                            fixed_divisor_bad_subsets
                                            != bad_direction_subsets
                                        ):
                                            raise AssertionError(
                                                {
                                                    "kind": (
                                                        "productive-"
                                                        if productive
                                                        else ""
                                                    )
                                                    + "marked-core-deficit-"
                                                    "anchor-direction-mds-"
                                                    "fixed-divisor-failed",
                                                    "p": p,
                                                    "k": k,
                                                    "syndrome": list(syn),
                                                    "fixed_roots": list(
                                                        fixed_roots
                                                    ),
                                                    "unmarked_core": list(
                                                        unmarked_core
                                                    ),
                                                    "marked_count": marked_count,
                                                    "core_deficit": core_deficit,
                                                    "anchor": list(anchor),
                                                    "direction_dim": (
                                                        residual_direction_dim
                                                    ),
                                                    "bad_subsets": [
                                                        list(item)
                                                        for item in sorted(
                                                            bad_direction_subsets
                                                        )
                                                    ],
                                                    "fixed_divisor_bad_subsets": [
                                                        list(item)
                                                        for item in sorted(
                                                            fixed_divisor_bad_subsets
                                                        )
                                                    ],
                                                }
                                            )
                                        projective_direction_count = (
                                            (p**residual_direction_dim - 1)
                                            // (p - 1)
                                        )
                                        per_direction_root_subsets = (
                                            binomial_or_zero(
                                                min(
                                                    len(available_roots),
                                                    residual_size - 1,
                                                ),
                                                residual_direction_dim,
                                            )
                                        )
                                        projective_root_count_bound = (
                                            projective_direction_count
                                            * per_direction_root_subsets
                                        )
                                        if (
                                            len(bad_direction_subsets)
                                            > projective_root_count_bound
                                        ):
                                            raise AssertionError(
                                                {
                                                    "kind": (
                                                        "productive-"
                                                        if productive
                                                        else ""
                                                    )
                                                    + "marked-core-deficit-"
                                                    "anchor-direction-mds-"
                                                    "projective-root-count-"
                                                    "bound-failed",
                                                    "p": p,
                                                    "k": k,
                                                    "syndrome": list(syn),
                                                    "fixed_roots": list(
                                                        fixed_roots
                                                    ),
                                                    "unmarked_core": list(
                                                        unmarked_core
                                                    ),
                                                    "marked_count": marked_count,
                                                    "core_deficit": core_deficit,
                                                    "anchor": list(anchor),
                                                    "direction_dim": (
                                                        residual_direction_dim
                                                    ),
                                                    "bad_subset_count": len(
                                                        bad_direction_subsets
                                                    ),
                                                    "projective_direction_count": (
                                                        projective_direction_count
                                                    ),
                                                    "per_direction_root_subsets": (
                                                        per_direction_root_subsets
                                                    ),
                                                    "bound": (
                                                        projective_root_count_bound
                                                    ),
                                                }
                                            )
                                        root_slice_bad_direction_subsets = set(
                                            itertools.combinations(
                                                sorted(root_slice_bad_roots),
                                                residual_direction_dim,
                                            )
                                        )
                                        if not bad_direction_subsets.issubset(
                                            root_slice_bad_direction_subsets
                                        ):
                                            raise AssertionError(
                                                {
                                                    "kind": (
                                                        "productive-"
                                                        if productive
                                                        else ""
                                                    )
                                                    + "marked-core-deficit-"
                                                    "anchor-direction-mds-"
                                                    "root-slice-envelope-"
                                                    "failed",
                                                    "p": p,
                                                    "k": k,
                                                    "syndrome": list(syn),
                                                    "fixed_roots": list(
                                                        fixed_roots
                                                    ),
                                                    "unmarked_core": list(
                                                        unmarked_core
                                                    ),
                                                    "marked_count": marked_count,
                                                    "core_deficit": core_deficit,
                                                    "anchor": list(anchor),
                                                    "direction_dim": (
                                                        residual_direction_dim
                                                    ),
                                                    "bad_subsets": [
                                                        list(item)
                                                        for item in sorted(
                                                            bad_direction_subsets
                                                        )
                                                    ],
                                                    "root_slice_bad_roots": (
                                                        sorted(
                                                            root_slice_bad_roots
                                                        )
                                                    ),
                                                }
                                            )
                                        if residual_direction_dim >= 2:
                                            if root_slice_bad_roots != set(
                                                available_roots
                                            ):
                                                raise AssertionError(
                                                    {
                                                        "kind": (
                                                            "productive-"
                                                            if productive
                                                            else ""
                                                        )
                                                        + "marked-core-"
                                                        "deficit-anchor-"
                                                        "direction-mds-"
                                                        "root-slice-full-"
                                                        "failed",
                                                        "p": p,
                                                        "k": k,
                                                        "syndrome": list(syn),
                                                        "fixed_roots": list(
                                                            fixed_roots
                                                        ),
                                                        "unmarked_core": list(
                                                            unmarked_core
                                                        ),
                                                        "marked_count": (
                                                            marked_count
                                                        ),
                                                        "core_deficit": (
                                                            core_deficit
                                                        ),
                                                        "anchor": list(anchor),
                                                        "direction_dim": (
                                                            residual_direction_dim
                                                        ),
                                                        "available_roots": list(
                                                            available_roots
                                                        ),
                                                        "root_slice_bad_roots": (
                                                            sorted(
                                                                root_slice_bad_roots
                                                            )
                                                        ),
                                                    }
                                                )
                                            if (
                                                p >= residual_size
                                                and not root_slice_persistent
                                            ):
                                                raise AssertionError(
                                                    {
                                                        "kind": (
                                                            "productive-"
                                                            if productive
                                                            else ""
                                                        )
                                                        + "marked-core-"
                                                        "deficit-anchor-"
                                                        "direction-mds-"
                                                        "persistence-"
                                                        "equivalence-failed",
                                                        "p": p,
                                                        "k": k,
                                                        "syndrome": list(syn),
                                                        "fixed_roots": list(
                                                            fixed_roots
                                                        ),
                                                        "unmarked_core": list(
                                                            unmarked_core
                                                        ),
                                                        "marked_count": (
                                                            marked_count
                                                        ),
                                                        "core_deficit": (
                                                            core_deficit
                                                        ),
                                                        "anchor": list(anchor),
                                                        "direction_dim": (
                                                            residual_direction_dim
                                                        ),
                                                        "available_roots": list(
                                                            available_roots
                                                        ),
                                                        "root_slice_bad_roots": (
                                                            sorted(
                                                                root_slice_bad_roots
                                                            )
                                                        ),
                                                    }
                                                )
                                        if residual_direction_dim == 2:
                                            projective_eval_base_roots: set[
                                                int
                                            ] = set()
                                            projective_eval_values: dict[
                                                int,
                                                tuple[int, ...],
                                            ] = {}
                                            projective_eval_fibers: dict[
                                                tuple[int, ...],
                                                list[int],
                                            ] = {}
                                            for root in available_roots:
                                                values = tuple(
                                                    polynomial_eval_mod(
                                                        vector,
                                                        domain[root],
                                                        p,
                                                    )
                                                    for vector in (
                                                        direction_basis
                                                    )
                                                )
                                                pivot = next(
                                                    (
                                                        value
                                                        for value in values
                                                        if value % p
                                                    ),
                                                    None,
                                                )
                                                if pivot is None:
                                                    projective_eval_base_roots.add(
                                                        root
                                                    )
                                                    continue
                                                inverse_pivot = pow(
                                                    pivot,
                                                    -1,
                                                    p,
                                                )
                                                key = tuple(
                                                    (value * inverse_pivot) % p
                                                    for value in values
                                                )
                                                projective_eval_values[root] = key
                                                projective_eval_fibers.setdefault(
                                                    key,
                                                    [],
                                                ).append(root)

                                            def check_half_height_quotient_shadow(
                                                roots: Sequence[int],
                                                direction: Sequence[int],
                                                shadow_kind: str,
                                                key: tuple[int, ...]
                                                | None = None,
                                                basis_index: int | None = None,
                                            ) -> None:
                                                root_tuple = tuple(
                                                    sorted(roots)
                                                )
                                                if (
                                                    2 * len(root_tuple)
                                                    < residual_size
                                                ):
                                                    return
                                                shadow_locator = cached_locator(
                                                    root_tuple
                                                )
                                                quotient_direction = (
                                                    divide_by_polynomial_exact_mod(
                                                        direction,
                                                        shadow_locator,
                                                        p,
                                                    )
                                                )
                                                quotient_width = (
                                                    residual_size
                                                    - len(root_tuple)
                                                )
                                                if (
                                                    len(quotient_direction)
                                                    != quotient_width
                                                    or 2 * quotient_width
                                                    > residual_size
                                                ):
                                                    raise AssertionError(
                                                        {
                                                            "kind": (
                                                                "productive-"
                                                                if productive
                                                                else ""
                                                            )
                                                            + "marked-core-"
                                                            "deficit-anchor-"
                                                            "direction-mds-"
                                                            "projective-"
                                                            "half-height-"
                                                            "quotient-width-"
                                                            "failed",
                                                            "p": p,
                                                            "k": k,
                                                            "syndrome": list(
                                                                syn
                                                            ),
                                                            "fixed_roots": list(
                                                                fixed_roots
                                                            ),
                                                            "unmarked_core": list(
                                                                unmarked_core
                                                            ),
                                                            "marked_count": (
                                                                marked_count
                                                            ),
                                                            "core_deficit": (
                                                                core_deficit
                                                            ),
                                                            "anchor": list(
                                                                anchor
                                                            ),
                                                            "shadow_kind": (
                                                                shadow_kind
                                                            ),
                                                            "key": (
                                                                list(key)
                                                                if key
                                                                is not None
                                                                else None
                                                            ),
                                                            "basis_index": (
                                                                basis_index
                                                            ),
                                                            "shadow_roots": list(
                                                                root_tuple
                                                            ),
                                                            "quotient_width": (
                                                                quotient_width
                                                            ),
                                                            "residual_size": (
                                                                residual_size
                                                            ),
                                                            "quotient": list(
                                                                quotient_direction
                                                            ),
                                                        }
                                                    )
                                                reconstructed_direction = (
                                                    multiply_polynomials_mod(
                                                        shadow_locator,
                                                        quotient_direction,
                                                        p,
                                                    )
                                                )
                                                if (
                                                    reconstructed_direction
                                                    != tuple(
                                                        value % p
                                                        for value in direction
                                                    )
                                                ):
                                                    raise AssertionError(
                                                        {
                                                            "kind": (
                                                                "productive-"
                                                                if productive
                                                                else ""
                                                            )
                                                            + "marked-core-"
                                                            "deficit-anchor-"
                                                            "direction-mds-"
                                                            "projective-"
                                                            "half-height-"
                                                            "quotient-"
                                                            "reconstruction-"
                                                            "failed",
                                                            "p": p,
                                                            "k": k,
                                                            "syndrome": list(
                                                                syn
                                                            ),
                                                            "fixed_roots": list(
                                                                fixed_roots
                                                            ),
                                                            "unmarked_core": list(
                                                                unmarked_core
                                                            ),
                                                            "marked_count": (
                                                                marked_count
                                                            ),
                                                            "core_deficit": (
                                                                core_deficit
                                                            ),
                                                            "anchor": list(
                                                                anchor
                                                            ),
                                                            "shadow_kind": (
                                                                shadow_kind
                                                            ),
                                                            "key": (
                                                                list(key)
                                                                if key
                                                                is not None
                                                                else None
                                                            ),
                                                            "basis_index": (
                                                                basis_index
                                                            ),
                                                            "shadow_roots": list(
                                                                root_tuple
                                                            ),
                                                            "direction": list(
                                                                direction
                                                            ),
                                                            "reconstructed": list(
                                                                reconstructed_direction
                                                            ),
                                                        }
                                                    )
                                                short_divisor = (
                                                    multiply_polynomials_mod(
                                                        anchor_locator,
                                                        shadow_locator,
                                                        p,
                                                    )
                                                )
                                                short_product = (
                                                    multiply_polynomials_mod(
                                                        short_divisor,
                                                        quotient_direction,
                                                        p,
                                                    )
                                                )
                                                short_vector = hankel_apply(
                                                    syn,
                                                    short_product,
                                                    residual_size,
                                                    p,
                                                )
                                                if any(short_vector):
                                                    raise AssertionError(
                                                        {
                                                            "kind": (
                                                                "productive-"
                                                                if productive
                                                                else ""
                                                            )
                                                            + "marked-core-"
                                                            "deficit-anchor-"
                                                            "direction-mds-"
                                                            "projective-"
                                                            "half-height-"
                                                            "quotient-kernel-"
                                                            "failed",
                                                            "p": p,
                                                            "k": k,
                                                            "syndrome": list(
                                                                syn
                                                            ),
                                                            "fixed_roots": list(
                                                                fixed_roots
                                                            ),
                                                            "unmarked_core": list(
                                                                unmarked_core
                                                            ),
                                                            "marked_count": (
                                                                marked_count
                                                            ),
                                                            "core_deficit": (
                                                                core_deficit
                                                            ),
                                                            "anchor": list(
                                                                anchor
                                                            ),
                                                            "shadow_kind": (
                                                                shadow_kind
                                                            ),
                                                            "key": (
                                                                list(key)
                                                                if key
                                                                is not None
                                                                else None
                                                            ),
                                                            "basis_index": (
                                                                basis_index
                                                            ),
                                                            "shadow_roots": list(
                                                                root_tuple
                                                            ),
                                                            "shadow_locator": list(
                                                                shadow_locator
                                                            ),
                                                            "quotient": list(
                                                                quotient_direction
                                                            ),
                                                            "short_vector": list(
                                                                short_vector
                                                            ),
                                                        }
                                                    )
                                            for root in (
                                                projective_eval_base_roots
                                            ):
                                                for vector in direction_basis:
                                                    if polynomial_eval_mod(
                                                        vector,
                                                        domain[root],
                                                        p,
                                                    ):
                                                        raise AssertionError(
                                                            {
                                                                "kind": (
                                                                    "productive-"
                                                                    if productive
                                                                    else ""
                                                                )
                                                                + "marked-core-"
                                                                "deficit-"
                                                                "anchor-"
                                                                "direction-"
                                                                "mds-"
                                                                "projective-"
                                                                "base-root-"
                                                                "slice-"
                                                                "failed",
                                                                "p": p,
                                                                "k": k,
                                                                "syndrome": list(
                                                                    syn
                                                                ),
                                                                "fixed_roots": list(
                                                                    fixed_roots
                                                                ),
                                                                "unmarked_core": list(
                                                                    unmarked_core
                                                                ),
                                                                "marked_count": (
                                                                    marked_count
                                                                ),
                                                                "core_deficit": (
                                                                    core_deficit
                                                                ),
                                                                "anchor": list(
                                                                    anchor
                                                                ),
                                                                "root": root,
                                                                "vector": list(
                                                                    vector
                                                                ),
                                                            }
                                                        )
                                            for basis_index, vector in enumerate(
                                                direction_basis
                                            ):
                                                check_half_height_quotient_shadow(
                                                    projective_eval_base_roots,
                                                    vector,
                                                    "base",
                                                    basis_index=basis_index,
                                                )
                                            if (
                                                2
                                                * len(
                                                    projective_eval_base_roots
                                                )
                                                >= residual_size
                                            ):
                                                base_root_tuple = tuple(
                                                    sorted(
                                                        projective_eval_base_roots
                                                    )
                                                )
                                                base_locator = cached_locator(
                                                    base_root_tuple
                                                )
                                                base_quotient_basis = tuple(
                                                    divide_by_polynomial_exact_mod(
                                                        vector,
                                                        base_locator,
                                                        p,
                                                    )
                                                    for vector in (
                                                        direction_basis
                                                    )
                                                )
                                                base_quotient_width = (
                                                    residual_size
                                                    - len(base_root_tuple)
                                                )
                                                base_quotient_rank = matrix_rank_mod(
                                                    base_quotient_basis,
                                                    p,
                                                )
                                                if (
                                                    any(
                                                        len(vector)
                                                        != base_quotient_width
                                                        for vector in (
                                                            base_quotient_basis
                                                        )
                                                    )
                                                    or base_quotient_rank
                                                    != residual_direction_dim
                                                ):
                                                    raise AssertionError(
                                                        {
                                                            "kind": (
                                                                "productive-"
                                                                if productive
                                                                else ""
                                                            )
                                                            + "marked-core-"
                                                            "deficit-anchor-"
                                                            "direction-mds-"
                                                            "projective-"
                                                            "base-quotient-"
                                                            "pencil-rank-"
                                                            "failed",
                                                            "p": p,
                                                            "k": k,
                                                            "syndrome": list(
                                                                syn
                                                            ),
                                                            "fixed_roots": list(
                                                                fixed_roots
                                                            ),
                                                            "unmarked_core": list(
                                                                unmarked_core
                                                            ),
                                                            "marked_count": (
                                                                marked_count
                                                            ),
                                                            "core_deficit": (
                                                                core_deficit
                                                            ),
                                                            "anchor": list(
                                                                anchor
                                                            ),
                                                            "base_roots": list(
                                                                base_root_tuple
                                                            ),
                                                            "quotient_width": (
                                                                base_quotient_width
                                                            ),
                                                            "quotient_basis": [
                                                                list(vector)
                                                                for vector in (
                                                                    base_quotient_basis
                                                                )
                                                            ],
                                                            "rank": (
                                                                base_quotient_rank
                                                            ),
                                                        }
                                                    )
                                                for root in available_roots:
                                                    if (
                                                        root
                                                        in projective_eval_base_roots
                                                    ):
                                                        continue
                                                    base_value = (
                                                        polynomial_eval_mod(
                                                            base_locator,
                                                            domain[root],
                                                            p,
                                                        )
                                                    )
                                                    if not base_value:
                                                        raise AssertionError(
                                                            {
                                                                "kind": (
                                                                    "productive-"
                                                                    if productive
                                                                    else ""
                                                                )
                                                                + "marked-core-"
                                                                "deficit-"
                                                                "anchor-"
                                                                "direction-"
                                                                "mds-"
                                                                "projective-"
                                                                "base-"
                                                                "quotient-"
                                                                "new-base-"
                                                                "failed",
                                                                "p": p,
                                                                "k": k,
                                                                "syndrome": list(
                                                                    syn
                                                                ),
                                                                "fixed_roots": list(
                                                                    fixed_roots
                                                                ),
                                                                "unmarked_core": list(
                                                                    unmarked_core
                                                                ),
                                                                "marked_count": (
                                                                    marked_count
                                                                ),
                                                                "core_deficit": (
                                                                    core_deficit
                                                                ),
                                                                "anchor": list(
                                                                    anchor
                                                                ),
                                                                "base_roots": list(
                                                                    base_root_tuple
                                                                ),
                                                                "root": root,
                                                            }
                                                        )
                                                    quotient_values = tuple(
                                                        polynomial_eval_mod(
                                                            vector,
                                                            domain[root],
                                                            p,
                                                        )
                                                        for vector in (
                                                            base_quotient_basis
                                                        )
                                                    )
                                                    direction_values = tuple(
                                                        polynomial_eval_mod(
                                                            vector,
                                                            domain[root],
                                                            p,
                                                        )
                                                        for vector in (
                                                            direction_basis
                                                        )
                                                    )
                                                    expected_values = tuple(
                                                        (
                                                            base_value * value
                                                        )
                                                        % p
                                                        for value in (
                                                            quotient_values
                                                        )
                                                    )
                                                    if (
                                                        direction_values
                                                        != expected_values
                                                    ):
                                                        raise AssertionError(
                                                            {
                                                                "kind": (
                                                                    "productive-"
                                                                    if productive
                                                                    else ""
                                                                )
                                                                + "marked-core-"
                                                                "deficit-"
                                                                "anchor-"
                                                                "direction-"
                                                                "mds-"
                                                                "projective-"
                                                                "base-"
                                                                "quotient-"
                                                                "evaluation-"
                                                                "failed",
                                                                "p": p,
                                                                "k": k,
                                                                "syndrome": list(
                                                                    syn
                                                                ),
                                                                "fixed_roots": list(
                                                                    fixed_roots
                                                                ),
                                                                "unmarked_core": list(
                                                                    unmarked_core
                                                                ),
                                                                "marked_count": (
                                                                    marked_count
                                                                ),
                                                                "core_deficit": (
                                                                    core_deficit
                                                                ),
                                                                "anchor": list(
                                                                    anchor
                                                                ),
                                                                "base_roots": list(
                                                                    base_root_tuple
                                                                ),
                                                                "root": root,
                                                                "direction_values": list(
                                                                    direction_values
                                                                ),
                                                                "expected_values": list(
                                                                    expected_values
                                                                ),
                                                            }
                                                        )
                                                    pivot = next(
                                                        (
                                                            value
                                                            for value in (
                                                                quotient_values
                                                            )
                                                            if value % p
                                                        ),
                                                        None,
                                                    )
                                                    if pivot is None:
                                                        raise AssertionError(
                                                            {
                                                                "kind": (
                                                                    "productive-"
                                                                    if productive
                                                                    else ""
                                                                )
                                                                + "marked-core-"
                                                                "deficit-"
                                                                "anchor-"
                                                                "direction-"
                                                                "mds-"
                                                                "projective-"
                                                                "base-"
                                                                "quotient-"
                                                                "zero-fiber-"
                                                                "failed",
                                                                "p": p,
                                                                "k": k,
                                                                "syndrome": list(
                                                                    syn
                                                                ),
                                                                "fixed_roots": list(
                                                                    fixed_roots
                                                                ),
                                                                "unmarked_core": list(
                                                                    unmarked_core
                                                                ),
                                                                "marked_count": (
                                                                    marked_count
                                                                ),
                                                                "core_deficit": (
                                                                    core_deficit
                                                                ),
                                                                "anchor": list(
                                                                    anchor
                                                                ),
                                                                "base_roots": list(
                                                                    base_root_tuple
                                                                ),
                                                                "root": root,
                                                            }
                                                        )
                                                    inverse_pivot = pow(
                                                        pivot,
                                                        -1,
                                                        p,
                                                    )
                                                    quotient_key = tuple(
                                                        (
                                                            value
                                                            * inverse_pivot
                                                        )
                                                        % p
                                                        for value in (
                                                            quotient_values
                                                        )
                                                    )
                                                    if (
                                                        quotient_key
                                                        != projective_eval_values[
                                                            root
                                                        ]
                                                    ):
                                                        raise AssertionError(
                                                            {
                                                                "kind": (
                                                                    "productive-"
                                                                    if productive
                                                                    else ""
                                                                )
                                                                + "marked-core-"
                                                                "deficit-"
                                                                "anchor-"
                                                                "direction-"
                                                                "mds-"
                                                                "projective-"
                                                                "base-"
                                                                "quotient-"
                                                                "fiber-map-"
                                                                "failed",
                                                                "p": p,
                                                                "k": k,
                                                                "syndrome": list(
                                                                    syn
                                                                ),
                                                                "fixed_roots": list(
                                                                    fixed_roots
                                                                ),
                                                                "unmarked_core": list(
                                                                    unmarked_core
                                                                ),
                                                                "marked_count": (
                                                                    marked_count
                                                                ),
                                                                "core_deficit": (
                                                                    core_deficit
                                                                ),
                                                                "anchor": list(
                                                                    anchor
                                                                ),
                                                                "base_roots": list(
                                                                    base_root_tuple
                                                                ),
                                                                "root": root,
                                                                "quotient_key": list(
                                                                    quotient_key
                                                                ),
                                                                "projective_key": list(
                                                                    projective_eval_values[
                                                                        root
                                                                    ]
                                                                ),
                                                            }
                                                        )
                                            projective_fiber_directions: dict[
                                                tuple[int, ...],
                                                tuple[int, ...],
                                            ] = {}
                                            for key, roots in (
                                                projective_eval_fibers.items()
                                            ):
                                                fiber_direction = tuple(
                                                    (
                                                        key[1]
                                                        * direction_basis[0][
                                                            index
                                                        ]
                                                        - key[0]
                                                        * direction_basis[1][
                                                            index
                                                        ]
                                                    )
                                                    % p
                                                    for index in range(
                                                        len(
                                                            direction_basis[0]
                                                        )
                                                    )
                                                )
                                                if not any(
                                                    fiber_direction
                                                ):
                                                    raise AssertionError(
                                                        {
                                                            "kind": (
                                                                "productive-"
                                                                if productive
                                                                else ""
                                                            )
                                                            + "marked-core-"
                                                            "deficit-anchor-"
                                                            "direction-mds-"
                                                            "projective-"
                                                            "fiber-slice-"
                                                            "zero-failed",
                                                            "p": p,
                                                            "k": k,
                                                            "syndrome": list(
                                                                syn
                                                            ),
                                                            "fixed_roots": list(
                                                                fixed_roots
                                                            ),
                                                            "unmarked_core": list(
                                                                unmarked_core
                                                            ),
                                                            "marked_count": (
                                                                marked_count
                                                            ),
                                                            "core_deficit": (
                                                                core_deficit
                                                            ),
                                                            "anchor": list(
                                                                anchor
                                                            ),
                                                            "key": list(key),
                                                        }
                                                    )
                                                for root in roots:
                                                    if polynomial_eval_mod(
                                                        fiber_direction,
                                                        domain[root],
                                                        p,
                                                    ):
                                                        raise AssertionError(
                                                            {
                                                                "kind": (
                                                                    "productive-"
                                                                    if productive
                                                                    else ""
                                                                )
                                                                + "marked-core-"
                                                                "deficit-"
                                                                "anchor-"
                                                                "direction-"
                                                                "mds-"
                                                                "projective-"
                                                                "fiber-slice-"
                                                                "failed",
                                                                "p": p,
                                                                "k": k,
                                                                "syndrome": list(
                                                                    syn
                                                                ),
                                                                "fixed_roots": list(
                                                                    fixed_roots
                                                                ),
                                                                "unmarked_core": list(
                                                                    unmarked_core
                                                                ),
                                                                "marked_count": (
                                                                    marked_count
                                                                ),
                                                                "core_deficit": (
                                                                    core_deficit
                                                                ),
                                                                "anchor": list(
                                                                    anchor
                                                                ),
                                                                "key": list(key),
                                                                "root": root,
                                                                "direction": list(
                                                                    fiber_direction
                                                                ),
                                                            }
                                                        )
                                                check_half_height_quotient_shadow(
                                                    roots,
                                                    fiber_direction,
                                                    "fiber",
                                                    key=key,
                                                )
                                                projective_fiber_directions[
                                                    key
                                                ] = fiber_direction
                                            projective_pair_bad_subsets: set[
                                                tuple[int, ...]
                                            ] = set()
                                            for left, right in (
                                                itertools.combinations(
                                                    available_roots,
                                                    2,
                                                )
                                            ):
                                                if (
                                                    left
                                                    in projective_eval_base_roots
                                                    or right
                                                    in projective_eval_base_roots
                                                    or projective_eval_values[
                                                        left
                                                    ]
                                                    == projective_eval_values[
                                                        right
                                                    ]
                                                ):
                                                    projective_pair_bad_subsets.add(
                                                        (left, right)
                                                    )
                                            if (
                                                projective_pair_bad_subsets
                                                != bad_direction_subsets
                                            ):
                                                raise AssertionError(
                                                    {
                                                        "kind": (
                                                            "productive-"
                                                            if productive
                                                            else ""
                                                        )
                                                        + "marked-core-"
                                                        "deficit-anchor-"
                                                        "direction-mds-"
                                                        "projective-fiber-"
                                                        "failed",
                                                        "p": p,
                                                        "k": k,
                                                        "syndrome": list(syn),
                                                        "fixed_roots": list(
                                                            fixed_roots
                                                        ),
                                                        "unmarked_core": list(
                                                            unmarked_core
                                                        ),
                                                        "marked_count": (
                                                            marked_count
                                                        ),
                                                        "core_deficit": (
                                                            core_deficit
                                                        ),
                                                        "anchor": list(anchor),
                                                        "bad_subsets": [
                                                            list(item)
                                                            for item in sorted(
                                                                bad_direction_subsets
                                                            )
                                                        ],
                                                        "projective_pair_bad_subsets": [
                                                            list(item)
                                                            for item in sorted(
                                                                projective_pair_bad_subsets
                                                            )
                                                        ],
                                                        "base_roots": sorted(
                                                            projective_eval_base_roots
                                                        ),
                                                        "fibers": {
                                                            str(key): sorted(
                                                                roots
                                                            )
                                                            for key, roots in (
                                                                projective_eval_fibers.items()
                                                            )
                                                        },
                                                    }
                                                )
                                            projective_base_pair_count = (
                                                math.comb(
                                                    len(available_roots),
                                                    2,
                                                )
                                                - math.comb(
                                                    (
                                                        len(available_roots)
                                                        - len(
                                                            projective_eval_base_roots
                                                        )
                                                    ),
                                                    2,
                                                )
                                            )
                                            projective_fiber_pair_count = sum(
                                                math.comb(len(roots), 2)
                                                for roots in (
                                                    projective_eval_fibers.values()
                                                )
                                            )
                                            projective_pair_count = (
                                                projective_base_pair_count
                                                + projective_fiber_pair_count
                                            )
                                            if (
                                                projective_pair_count
                                                != len(bad_direction_subsets)
                                            ):
                                                raise AssertionError(
                                                    {
                                                        "kind": (
                                                            "productive-"
                                                            if productive
                                                            else ""
                                                        )
                                                        + "marked-core-"
                                                        "deficit-anchor-"
                                                        "direction-mds-"
                                                        "projective-fiber-"
                                                        "count-failed",
                                                        "p": p,
                                                        "k": k,
                                                        "syndrome": list(syn),
                                                        "fixed_roots": list(
                                                            fixed_roots
                                                        ),
                                                        "unmarked_core": list(
                                                            unmarked_core
                                                        ),
                                                        "marked_count": (
                                                            marked_count
                                                        ),
                                                        "core_deficit": (
                                                            core_deficit
                                                        ),
                                                        "anchor": list(anchor),
                                                        "bad_subset_count": len(
                                                            bad_direction_subsets
                                                        ),
                                                        "base_pair_count": (
                                                            projective_base_pair_count
                                                        ),
                                                        "fiber_pair_count": (
                                                            projective_fiber_pair_count
                                                        ),
                                                        "base_roots": sorted(
                                                            projective_eval_base_roots
                                                        ),
                                                        "fibers": {
                                                            str(key): sorted(
                                                                roots
                                                            )
                                                            for key, roots in (
                                                                projective_eval_fibers.items()
                                                            )
                                                        },
                                                    }
                                                )
                                            max_projective_fiber_size = max(
                                                (
                                                    len(roots)
                                                    for roots in (
                                                        projective_eval_fibers.values()
                                                    )
                                                ),
                                                default=0,
                                            )
                                            projective_root_shadow_height = max(
                                                len(
                                                    projective_eval_base_roots
                                                ),
                                                max_projective_fiber_size,
                                            )
                                            if (
                                                max_projective_fiber_size
                                                > residual_size - 1
                                                or len(
                                                    projective_eval_base_roots
                                                )
                                                > residual_size - 1
                                            ):
                                                raise AssertionError(
                                                    {
                                                        "kind": (
                                                            "productive-"
                                                            if productive
                                                            else ""
                                                        )
                                                        + "marked-core-"
                                                        "deficit-anchor-"
                                                        "direction-mds-"
                                                        "projective-fiber-"
                                                        "degree-bound-failed",
                                                        "p": p,
                                                        "k": k,
                                                        "syndrome": list(syn),
                                                        "fixed_roots": list(
                                                            fixed_roots
                                                        ),
                                                        "unmarked_core": list(
                                                            unmarked_core
                                                        ),
                                                        "marked_count": (
                                                            marked_count
                                                        ),
                                                        "core_deficit": (
                                                            core_deficit
                                                        ),
                                                        "anchor": list(anchor),
                                                        "max_fiber_size": (
                                                            max_projective_fiber_size
                                                        ),
                                                        "base_roots": sorted(
                                                            projective_eval_base_roots
                                                        ),
                                                        "bound": (
                                                            residual_size - 1
                                                        ),
                                                    }
                                                )
                                            nonbase_projective_root_count = (
                                                len(available_roots)
                                                - len(
                                                    projective_eval_base_roots
                                                )
                                            )
                                            projective_pair_envelope = (
                                                projective_base_pair_count
                                                + (
                                                    max_projective_fiber_size
                                                    - 1
                                                )
                                                * nonbase_projective_root_count
                                                // 2
                                            )
                                            if (
                                                len(bad_direction_subsets)
                                                > projective_pair_envelope
                                            ):
                                                raise AssertionError(
                                                    {
                                                        "kind": (
                                                            "productive-"
                                                            if productive
                                                            else ""
                                                        )
                                                        + "marked-core-"
                                                        "deficit-anchor-"
                                                        "direction-mds-"
                                                        "projective-fiber-"
                                                        "envelope-failed",
                                                        "p": p,
                                                        "k": k,
                                                        "syndrome": list(syn),
                                                        "fixed_roots": list(
                                                            fixed_roots
                                                        ),
                                                        "unmarked_core": list(
                                                            unmarked_core
                                                        ),
                                                        "marked_count": (
                                                            marked_count
                                                        ),
                                                        "core_deficit": (
                                                            core_deficit
                                                        ),
                                                        "anchor": list(anchor),
                                                        "bad_subset_count": len(
                                                            bad_direction_subsets
                                                        ),
                                                        "max_fiber_size": (
                                                            max_projective_fiber_size
                                                        ),
                                                        "base_pair_count": (
                                                            projective_base_pair_count
                                                        ),
                                                        "envelope": (
                                                            projective_pair_envelope
                                                        ),
                                                    }
                                                )
                                            projective_good_pairs: set[
                                                tuple[int, int]
                                            ] = set()
                                            for left, right in (
                                                itertools.combinations(
                                                    available_roots,
                                                    2,
                                                )
                                            ):
                                                if (
                                                    left
                                                    in projective_eval_base_roots
                                                    or right
                                                    in projective_eval_base_roots
                                                ):
                                                    continue
                                                if (
                                                    projective_eval_values[left]
                                                    != projective_eval_values[
                                                        right
                                                    ]
                                                ):
                                                    projective_good_pairs.add(
                                                        (left, right)
                                                    )
                                            expected_good_pair_count = (
                                                math.comb(
                                                    (
                                                        len(available_roots)
                                                        - len(
                                                            projective_eval_base_roots
                                                        )
                                                    ),
                                                    2,
                                                )
                                                - projective_fiber_pair_count
                                            )
                                            if (
                                                len(projective_good_pairs)
                                                != expected_good_pair_count
                                            ):
                                                raise AssertionError(
                                                    {
                                                        "kind": (
                                                            "productive-"
                                                            if productive
                                                            else ""
                                                        )
                                                        + "marked-core-"
                                                        "deficit-anchor-"
                                                        "direction-mds-"
                                                        "projective-good-pair-"
                                                        "count-failed",
                                                        "p": p,
                                                        "k": k,
                                                        "syndrome": list(syn),
                                                        "fixed_roots": list(
                                                            fixed_roots
                                                        ),
                                                        "unmarked_core": list(
                                                            unmarked_core
                                                        ),
                                                        "marked_count": (
                                                            marked_count
                                                        ),
                                                        "core_deficit": (
                                                            core_deficit
                                                        ),
                                                        "anchor": list(anchor),
                                                        "good_pair_count": len(
                                                            projective_good_pairs
                                                        ),
                                                        "expected": (
                                                            expected_good_pair_count
                                                        ),
                                                    }
                                                )
                                            projective_zero_good_envelope_count = (
                                                binomial_or_zero(
                                                    len(
                                                        projective_eval_base_roots
                                                    ),
                                                    residual_size,
                                                )
                                                + sum(
                                                    binomial_or_zero(
                                                        len(roots),
                                                        nonbase_count,
                                                    )
                                                    * binomial_or_zero(
                                                        len(
                                                            projective_eval_base_roots
                                                        ),
                                                        (
                                                            residual_size
                                                            - nonbase_count
                                                        ),
                                                    )
                                                    for roots in (
                                                        projective_eval_fibers.values()
                                                    )
                                                    for nonbase_count in range(
                                                        1,
                                                        min(
                                                            residual_size,
                                                            len(roots),
                                                        )
                                                        + 1,
                                                    )
                                                )
                                            )
                                            base_root_count = len(
                                                projective_eval_base_roots
                                            )
                                            projective_direction_shadow_sizes = (
                                                tuple(
                                                    sorted(
                                                        base_root_count
                                                        + len(roots)
                                                        for roots in (
                                                            projective_eval_fibers.values()
                                                        )
                                                    )
                                                )
                                            )
                                            projective_max_direction_shadow_size = (
                                                max(
                                                    (
                                                        base_root_count,
                                                        *projective_direction_shadow_sizes,
                                                    )
                                                )
                                            )
                                            projective_zero_good_shadow_count = (
                                                binomial_or_zero(
                                                    base_root_count,
                                                    residual_size,
                                                )
                                                + sum(
                                                    binomial_or_zero(
                                                        (
                                                            base_root_count
                                                            + len(roots)
                                                        ),
                                                        residual_size,
                                                    )
                                                    - binomial_or_zero(
                                                        base_root_count,
                                                        residual_size,
                                                    )
                                                    for roots in (
                                                        projective_eval_fibers.values()
                                                    )
                                                )
                                            )
                                            half_certificate_size = (
                                                residual_size + 1
                                            ) // 2
                                            projective_half_certificate_count = (
                                                binomial_or_zero(
                                                    len(
                                                        projective_eval_base_roots
                                                    ),
                                                    half_certificate_size,
                                                )
                                                + sum(
                                                    binomial_or_zero(
                                                        len(roots),
                                                        half_certificate_size,
                                                    )
                                                    for roots in (
                                                        projective_eval_fibers.values()
                                                    )
                                                )
                                            )
                                            projective_zero_good_incidence_bound = (
                                                projective_half_certificate_count
                                                * binomial_or_zero(
                                                    (
                                                        len(available_roots)
                                                        - half_certificate_size
                                                    ),
                                                    (
                                                        residual_size
                                                        - half_certificate_size
                                                    ),
                                                )
                                            )
                                            base_half_completion_count = (
                                                binomial_or_zero(
                                                    (
                                                        len(
                                                            projective_eval_base_roots
                                                        )
                                                        - half_certificate_size
                                                    ),
                                                    (
                                                        residual_size
                                                        - half_certificate_size
                                                    ),
                                                )
                                                + sum(
                                                    binomial_or_zero(
                                                        len(roots),
                                                        nonbase_count,
                                                    )
                                                    * binomial_or_zero(
                                                        (
                                                            len(
                                                                projective_eval_base_roots
                                                            )
                                                            - half_certificate_size
                                                        ),
                                                        (
                                                            residual_size
                                                            - half_certificate_size
                                                            - nonbase_count
                                                        ),
                                                    )
                                                    for roots in (
                                                        projective_eval_fibers.values()
                                                    )
                                                    for nonbase_count in range(
                                                        1,
                                                        (
                                                            residual_size
                                                            - half_certificate_size
                                                        )
                                                        + 1,
                                                    )
                                                )
                                            )
                                            fiber_half_incidence_bound = sum(
                                                binomial_or_zero(
                                                    len(roots),
                                                    half_certificate_size,
                                                )
                                                * sum(
                                                    binomial_or_zero(
                                                        (
                                                            len(roots)
                                                            - half_certificate_size
                                                        ),
                                                        same_fiber_count,
                                                    )
                                                    * binomial_or_zero(
                                                        len(
                                                            projective_eval_base_roots
                                                        ),
                                                        (
                                                            residual_size
                                                            - half_certificate_size
                                                            - same_fiber_count
                                                        ),
                                                    )
                                                    for same_fiber_count in range(
                                                        0,
                                                        (
                                                            residual_size
                                                            - half_certificate_size
                                                        )
                                                        + 1,
                                                    )
                                                )
                                                for roots in (
                                                    projective_eval_fibers.values()
                                                )
                                            )
                                            projective_zero_good_local_bound = (
                                                binomial_or_zero(
                                                    len(
                                                        projective_eval_base_roots
                                                    ),
                                                    half_certificate_size,
                                                )
                                                * base_half_completion_count
                                                + fiber_half_incidence_bound
                                            )

                                            def projective_local_error(
                                                suffix: str,
                                                **extra: object,
                                            ) -> dict[str, object]:
                                                payload: dict[str, object] = {
                                                    "kind": (
                                                        (
                                                            "productive-"
                                                            if productive
                                                            else ""
                                                        )
                                                        + "marked-core-"
                                                        "deficit-anchor-"
                                                        "direction-mds-"
                                                        "projective-"
                                                        + suffix
                                                    ),
                                                    "p": p,
                                                    "k": k,
                                                    "syndrome": list(syn),
                                                    "fixed_roots": list(
                                                        fixed_roots
                                                    ),
                                                    "unmarked_core": list(
                                                        unmarked_core
                                                    ),
                                                    "marked_count": marked_count,
                                                    "core_deficit": core_deficit,
                                                    "anchor": list(anchor),
                                                }
                                                payload.update(extra)
                                                return payload

                                            def check_dominant_slice_quotient(
                                                roots: Sequence[int],
                                                direction: Sequence[int],
                                                shadow_kind: str,
                                                expected_width: int,
                                                key: tuple[int, ...]
                                                | None = None,
                                                basis_index: int | None = None,
                                            ) -> None:
                                                root_tuple = tuple(sorted(roots))
                                                shadow_locator = cached_locator(
                                                    root_tuple
                                                )
                                                quotient_direction = (
                                                    divide_by_polynomial_exact_mod(
                                                        direction,
                                                        shadow_locator,
                                                        p,
                                                    )
                                                )
                                                quotient_width = (
                                                    residual_size
                                                    - len(root_tuple)
                                                )
                                                if (
                                                    quotient_width
                                                    != expected_width
                                                    or len(quotient_direction)
                                                    != quotient_width
                                                ):
                                                    raise AssertionError(
                                                        projective_local_error(
                                                            "dominant-slice-"
                                                            "quotient-width-"
                                                            "failed",
                                                            shadow_kind=(
                                                                shadow_kind
                                                            ),
                                                            key=(
                                                                list(key)
                                                                if key
                                                                is not None
                                                                else None
                                                            ),
                                                            basis_index=(
                                                                basis_index
                                                            ),
                                                            shadow_roots=list(
                                                                root_tuple
                                                            ),
                                                            quotient_width=(
                                                                quotient_width
                                                            ),
                                                            expected_width=(
                                                                expected_width
                                                            ),
                                                            quotient=list(
                                                                quotient_direction
                                                            ),
                                                        )
                                                    )
                                                reconstructed_direction = (
                                                    multiply_polynomials_mod(
                                                        shadow_locator,
                                                        quotient_direction,
                                                        p,
                                                    )
                                                )
                                                if reconstructed_direction != tuple(
                                                    value % p
                                                    for value in direction
                                                ):
                                                    raise AssertionError(
                                                        projective_local_error(
                                                            "dominant-slice-"
                                                            "quotient-"
                                                            "reconstruction-"
                                                            "failed",
                                                            shadow_kind=(
                                                                shadow_kind
                                                            ),
                                                            key=(
                                                                list(key)
                                                                if key
                                                                is not None
                                                                else None
                                                            ),
                                                            basis_index=(
                                                                basis_index
                                                            ),
                                                            shadow_roots=list(
                                                                root_tuple
                                                            ),
                                                            direction=list(
                                                                direction
                                                            ),
                                                            reconstructed=list(
                                                                reconstructed_direction
                                                            ),
                                                        )
                                                    )
                                                short_product = (
                                                    multiply_polynomials_mod(
                                                        anchor_locator,
                                                        direction,
                                                        p,
                                                    )
                                                )
                                                short_vector = hankel_apply(
                                                    syn,
                                                    short_product,
                                                    residual_size,
                                                    p,
                                                )
                                                if any(short_vector):
                                                    raise AssertionError(
                                                        projective_local_error(
                                                            "dominant-slice-"
                                                            "quotient-kernel-"
                                                            "failed",
                                                            shadow_kind=(
                                                                shadow_kind
                                                            ),
                                                            key=(
                                                                list(key)
                                                                if key
                                                                is not None
                                                                else None
                                                            ),
                                                            basis_index=(
                                                                basis_index
                                                            ),
                                                            shadow_roots=list(
                                                                root_tuple
                                                            ),
                                                            quotient=list(
                                                                quotient_direction
                                                            ),
                                                            short_vector=list(
                                                                short_vector
                                                            ),
                                                        )
                                                    )

                                            if (
                                                projective_zero_good_local_bound
                                                > projective_zero_good_incidence_bound
                                            ):
                                                raise AssertionError(
                                                    projective_local_error(
                                                        "zero-good-local-"
                                                        "incidence-dominance-"
                                                        "failed",
                                                        local_bound=(
                                                            projective_zero_good_local_bound
                                                        ),
                                                        global_bound=(
                                                            projective_zero_good_incidence_bound
                                                        ),
                                                    )
                                                )
                                            if (
                                                projective_zero_good_envelope_count
                                                > projective_zero_good_local_bound
                                            ):
                                                raise AssertionError(
                                                    projective_local_error(
                                                        "zero-good-local-"
                                                        "envelope-bound-failed",
                                                        zero_good_envelope=(
                                                            projective_zero_good_envelope_count
                                                        ),
                                                        local_bound=(
                                                            projective_zero_good_local_bound
                                                        ),
                                                        base_half_completion_count=(
                                                            base_half_completion_count
                                                        ),
                                                        fiber_half_incidence_bound=(
                                                            fiber_half_incidence_bound
                                                        ),
                                                    )
                                                )
                                            if (
                                                projective_zero_good_shadow_count
                                                != projective_zero_good_envelope_count
                                            ):
                                                raise AssertionError(
                                                    projective_local_error(
                                                        "zero-good-shadow-"
                                                        "identity-failed",
                                                        shadow_count=(
                                                            projective_zero_good_shadow_count
                                                        ),
                                                        envelope_count=(
                                                            projective_zero_good_envelope_count
                                                        ),
                                                        base_root_count=(
                                                            base_root_count
                                                        ),
                                                        shadow_sizes=(
                                                            projective_direction_shadow_sizes
                                                        ),
                                                    )
                                                )
                                            if (
                                                projective_max_direction_shadow_size
                                                >= residual_size
                                            ):
                                                raise AssertionError(
                                                    projective_local_error(
                                                        "zero-good-degree-"
                                                        "gap-failed",
                                                        residual_size=(
                                                            residual_size
                                                        ),
                                                        base_root_count=(
                                                            base_root_count
                                                        ),
                                                        max_shadow_size=(
                                                            projective_max_direction_shadow_size
                                                        ),
                                                        shadow_sizes=(
                                                            projective_direction_shadow_sizes
                                                        ),
                                                    )
                                                )
                                            if projective_zero_good_envelope_count:
                                                raise AssertionError(
                                                    projective_local_error(
                                                        "zero-good-envelope-"
                                                        "degree-gap-failed",
                                                        zero_good_envelope=(
                                                            projective_zero_good_envelope_count
                                                        ),
                                                        max_shadow_size=(
                                                            projective_max_direction_shadow_size
                                                        ),
                                                    )
                                                )

                                            def interpolate_good_pair_locator(
                                                pair: tuple[int, int],
                                            ) -> tuple[
                                                tuple[tuple[int, ...], ...],
                                                tuple[int, ...],
                                                tuple[int, ...],
                                            ]:
                                                interpolation_matrix = tuple(
                                                    tuple(
                                                        polynomial_eval_mod(
                                                            vector,
                                                            domain[root],
                                                            p,
                                                        )
                                                        for vector in (
                                                            direction_basis
                                                        )
                                                    )
                                                    for root in pair
                                                )
                                                origin_values = tuple(
                                                    polynomial_eval_mod(
                                                        residual_locator,
                                                        domain[root],
                                                        p,
                                                    )
                                                    for root in pair
                                                )
                                                interpolation_coeffs = (
                                                    solve_square_mod(
                                                        interpolation_matrix,
                                                        tuple(
                                                            (-value) % p
                                                            for value in (
                                                                origin_values
                                                            )
                                                        ),
                                                        p,
                                                    )
                                                )
                                                reconstructed_locator = tuple(
                                                    (
                                                        residual_locator[index]
                                                        + sum(
                                                            coeff * vector[index]
                                                            for (
                                                                coeff,
                                                                vector,
                                                            ) in zip(
                                                                interpolation_coeffs,
                                                                direction_basis,
                                                            )
                                                        )
                                                    )
                                                    % p
                                                    for index in range(
                                                        residual_size
                                                    )
                                                ) + (1,)
                                                return (
                                                    interpolation_matrix,
                                                    interpolation_coeffs,
                                                    reconstructed_locator,
                                                )

                                            def affine_kernel_row(
                                                root: int,
                                            ) -> tuple[int, int, int]:
                                                return (
                                                    polynomial_eval_mod(
                                                        residual_locator,
                                                        domain[root],
                                                        p,
                                                    ),
                                                    polynomial_eval_mod(
                                                        direction_basis[0],
                                                        domain[root],
                                                        p,
                                                    ),
                                                    polynomial_eval_mod(
                                                        direction_basis[1],
                                                        domain[root],
                                                        p,
                                                    ),
                                                )

                                            def direction_coeff(
                                                vector: tuple[int, ...],
                                                index: int,
                                            ) -> int:
                                                return (
                                                    vector[index]
                                                    if index < len(vector)
                                                    else 0
                                                )
                                            pair_owner: dict[
                                                tuple[int, int],
                                                tuple[int, ...],
                                            ] = {}
                                            candidate_good_pair_min: int | None = (
                                                None
                                            )
                                            candidate_base_occupancy_max = 0
                                            candidate_fiber_occupancy_max = 0
                                            zero_good_candidate_count = 0
                                            residual_candidate_set = set(
                                                residual_candidates
                                            )
                                            candidate_good_pair_counts: dict[
                                                tuple[int, ...],
                                                int,
                                            ] = {}
                                            for candidate in residual_candidates:
                                                candidate_locator = cached_locator(
                                                    candidate
                                                )
                                                candidate_good_pairs = 0
                                                candidate_base_occupancy = sum(
                                                    1
                                                    for root in candidate
                                                    if root
                                                    in projective_eval_base_roots
                                                )
                                                candidate_fiber_roots: dict[
                                                    tuple[int, ...],
                                                    list[int],
                                                ] = {}
                                                for root in candidate:
                                                    if (
                                                        root
                                                        in projective_eval_base_roots
                                                    ):
                                                        continue
                                                    key = projective_eval_values[
                                                        root
                                                    ]
                                                    candidate_fiber_roots.setdefault(
                                                        key,
                                                        [],
                                                    ).append(root)
                                                candidate_fiber_counts = {
                                                    key: len(roots)
                                                    for key, roots in (
                                                        candidate_fiber_roots.items()
                                                    )
                                                }
                                                candidate_base_occupancy_max = max(
                                                    candidate_base_occupancy_max,
                                                    candidate_base_occupancy,
                                                )
                                                candidate_fiber_occupancy_max = max(
                                                    candidate_fiber_occupancy_max,
                                                    max(
                                                        candidate_fiber_counts.values(),
                                                        default=0,
                                                    ),
                                                )
                                                for pair in itertools.combinations(
                                                    candidate,
                                                    2,
                                                ):
                                                    if pair not in (
                                                        projective_good_pairs
                                                    ):
                                                        continue
                                                    candidate_good_pairs += 1
                                                    (
                                                        interpolation_matrix,
                                                        interpolation_coeffs,
                                                        reconstructed_locator,
                                                    ) = interpolate_good_pair_locator(
                                                        pair
                                                    )
                                                    if (
                                                        reconstructed_locator
                                                        != candidate_locator
                                                    ):
                                                        raise AssertionError(
                                                            projective_local_error(
                                                                "good-pair-"
                                                                "interpolation-"
                                                                "failed",
                                                                candidate=list(
                                                                    candidate
                                                                ),
                                                                pair=list(pair),
                                                                matrix=[
                                                                    list(row)
                                                                    for row in (
                                                                        interpolation_matrix
                                                                    )
                                                                ],
                                                                coeffs=list(
                                                                    interpolation_coeffs
                                                                ),
                                                                reconstructed=list(
                                                                    reconstructed_locator
                                                                ),
                                                                expected=list(
                                                                    candidate_locator
                                                                ),
                                                            )
                                                        )
                                                    previous = pair_owner.get(
                                                        pair
                                                    )
                                                    if (
                                                        previous is not None
                                                        and previous != candidate
                                                    ):
                                                        raise AssertionError(
                                                            {
                                                                "kind": (
                                                                    "productive-"
                                                                    if productive
                                                                    else ""
                                                                )
                                                                + "marked-core-"
                                                                "deficit-"
                                                                "anchor-"
                                                                "direction-mds-"
                                                                "projective-"
                                                                "good-pair-"
                                                                "collision-"
                                                                "failed",
                                                                "p": p,
                                                                "k": k,
                                                                "syndrome": list(
                                                                    syn
                                                                ),
                                                                "fixed_roots": list(
                                                                    fixed_roots
                                                                ),
                                                                "unmarked_core": list(
                                                                    unmarked_core
                                                                ),
                                                                "marked_count": (
                                                                    marked_count
                                                                ),
                                                                "core_deficit": (
                                                                    core_deficit
                                                                ),
                                                                "anchor": list(
                                                                    anchor
                                                                ),
                                                                "pair": list(
                                                                    pair
                                                                ),
                                                                "left": list(
                                                                    previous
                                                                ),
                                                                "right": list(
                                                                    candidate
                                                                ),
                                                            }
                                                        )
                                                    pair_owner[pair] = candidate
                                                candidate_good_pair_min = (
                                                    candidate_good_pairs
                                                    if candidate_good_pair_min
                                                    is None
                                                    else min(
                                                        candidate_good_pair_min,
                                                        candidate_good_pairs,
                                                    )
                                                )
                                                candidate_good_pair_counts[
                                                    candidate
                                                ] = candidate_good_pairs
                                                nonbase_candidate_roots = (
                                                    residual_size
                                                    - candidate_base_occupancy
                                                )
                                                largest_candidate_fiber = max(
                                                    candidate_fiber_counts.values(),
                                                    default=0,
                                                )
                                                candidate_projective_escape = (
                                                    nonbase_candidate_roots
                                                    - largest_candidate_fiber
                                                )
                                                dominant_escape_lower = (
                                                    nonbase_candidate_roots
                                                    * candidate_projective_escape
                                                    + 1
                                                ) // 2
                                                expected_candidate_good_pairs = (
                                                    math.comb(
                                                        nonbase_candidate_roots,
                                                        2,
                                                    )
                                                    - sum(
                                                        math.comb(count, 2)
                                                        for count in (
                                                            candidate_fiber_counts.values()
                                                        )
                                                    )
                                                )
                                                if (
                                                    candidate_good_pairs
                                                    != expected_candidate_good_pairs
                                                ):
                                                    raise AssertionError(
                                                        {
                                                            "kind": (
                                                                "productive-"
                                                                if productive
                                                                else ""
                                                            )
                                                            + "marked-core-"
                                                            "deficit-anchor-"
                                                            "direction-mds-"
                                                            "projective-"
                                                            "candidate-good-"
                                                            "pair-count-"
                                                            "failed",
                                                            "p": p,
                                                            "k": k,
                                                            "syndrome": list(syn),
                                                            "fixed_roots": list(
                                                                fixed_roots
                                                            ),
                                                            "unmarked_core": list(
                                                                unmarked_core
                                                            ),
                                                            "marked_count": (
                                                                marked_count
                                                            ),
                                                            "core_deficit": (
                                                                core_deficit
                                                            ),
                                                            "anchor": list(anchor),
                                                            "candidate": list(
                                                                candidate
                                                            ),
                                                            "candidate_good_pairs": (
                                                                candidate_good_pairs
                                                            ),
                                                            "expected": (
                                                                expected_candidate_good_pairs
                                                            ),
                                                            "base_occupancy": (
                                                                candidate_base_occupancy
                                                            ),
                                                            "fiber_counts": {
                                                                str(key): count
                                                                for key, count in (
                                                                    candidate_fiber_counts.items()
                                                                )
                                                            },
                                                        }
                                                    )
                                                if (
                                                    candidate_good_pairs
                                                    < dominant_escape_lower
                                                ):
                                                    raise AssertionError(
                                                        {
                                                            "kind": (
                                                                "productive-"
                                                                if productive
                                                                else ""
                                                            )
                                                            + "marked-core-"
                                                            "deficit-anchor-"
                                                            "direction-mds-"
                                                            "projective-"
                                                            "dominant-fiber-"
                                                            "escape-lower-"
                                                            "bound-failed",
                                                            "p": p,
                                                            "k": k,
                                                            "syndrome": list(syn),
                                                            "fixed_roots": list(
                                                                fixed_roots
                                                            ),
                                                            "unmarked_core": list(
                                                                unmarked_core
                                                            ),
                                                            "marked_count": (
                                                                marked_count
                                                            ),
                                                            "core_deficit": (
                                                                core_deficit
                                                            ),
                                                            "anchor": list(anchor),
                                                            "candidate": list(
                                                                candidate
                                                            ),
                                                            "candidate_good_pairs": (
                                                                candidate_good_pairs
                                                            ),
                                                            "nonbase_roots": (
                                                                nonbase_candidate_roots
                                                            ),
                                                            "largest_fiber": (
                                                                largest_candidate_fiber
                                                            ),
                                                            "projective_escape": (
                                                                candidate_projective_escape
                                                            ),
                                                            "lower_bound": (
                                                                dominant_escape_lower
                                                            ),
                                                            "fiber_counts": {
                                                                str(key): count
                                                                for key, count in (
                                                                    candidate_fiber_counts.items()
                                                                )
                                                            },
                                                        }
                                                    )
                                                if (
                                                    candidate_base_occupancy
                                                    >= largest_candidate_fiber
                                                ):
                                                    dominant_base_roots = tuple(
                                                        root
                                                        for root in candidate
                                                        if root
                                                        in projective_eval_base_roots
                                                    )
                                                    dominant_width = (
                                                        residual_size
                                                        - candidate_base_occupancy
                                                    )
                                                    for (
                                                        basis_index,
                                                        vector,
                                                    ) in enumerate(
                                                        direction_basis
                                                    ):
                                                        check_dominant_slice_quotient(
                                                            dominant_base_roots,
                                                            vector,
                                                            "candidate-base",
                                                            dominant_width,
                                                            basis_index=(
                                                                basis_index
                                                            ),
                                                        )
                                                else:
                                                    (
                                                        dominant_key,
                                                        dominant_roots,
                                                    ) = max(
                                                        candidate_fiber_roots.items(),
                                                        key=lambda item: (
                                                            len(item[1]),
                                                            item[0],
                                                        ),
                                                    )
                                                    dominant_width = (
                                                        candidate_base_occupancy
                                                        + candidate_projective_escape
                                                    )
                                                    if (
                                                        dominant_width
                                                        != residual_size
                                                        - len(dominant_roots)
                                                    ):
                                                        raise AssertionError(
                                                            {
                                                                "kind": (
                                                                    "productive-"
                                                                    if productive
                                                                    else ""
                                                                )
                                                                + "marked-core-"
                                                                "deficit-anchor-"
                                                                "direction-mds-"
                                                                "projective-"
                                                                "dominant-fiber-"
                                                                "width-"
                                                                "identity-"
                                                                "failed",
                                                                "p": p,
                                                                "k": k,
                                                                "syndrome": list(
                                                                    syn
                                                                ),
                                                                "fixed_roots": list(
                                                                    fixed_roots
                                                                ),
                                                                "unmarked_core": list(
                                                                    unmarked_core
                                                                ),
                                                                "marked_count": (
                                                                    marked_count
                                                                ),
                                                                "core_deficit": (
                                                                    core_deficit
                                                                ),
                                                                "anchor": list(
                                                                    anchor
                                                                ),
                                                                "candidate": list(
                                                                    candidate
                                                                ),
                                                                "dominant_roots": list(
                                                                    dominant_roots
                                                                ),
                                                                "base_occupancy": (
                                                                    candidate_base_occupancy
                                                                ),
                                                                "projective_escape": (
                                                                    candidate_projective_escape
                                                                ),
                                                                "dominant_width": (
                                                                    dominant_width
                                                                ),
                                                            }
                                                        )
                                                    check_dominant_slice_quotient(
                                                        dominant_roots,
                                                        projective_fiber_directions[
                                                            dominant_key
                                                        ],
                                                        "candidate-fiber",
                                                        dominant_width,
                                                        key=dominant_key,
                                                    )
                                                if candidate_good_pairs == 0:
                                                    zero_good_candidate_count += 1
                                                    support_base_roots = tuple(
                                                        root
                                                        for root in candidate
                                                        if root
                                                        in projective_eval_base_roots
                                                    )
                                                    support_certificate_count = 0
                                                    if (
                                                        2
                                                        * len(
                                                            support_base_roots
                                                        )
                                                        >= residual_size
                                                    ):
                                                        support_certificate_count += (
                                                            1
                                                        )
                                                        for (
                                                            basis_index,
                                                            vector,
                                                        ) in enumerate(
                                                            direction_basis
                                                        ):
                                                            check_half_height_quotient_shadow(
                                                                support_base_roots,
                                                                vector,
                                                                "support-base",
                                                                basis_index=(
                                                                    basis_index
                                                                ),
                                                            )
                                                    for key, roots in (
                                                        candidate_fiber_roots.items()
                                                    ):
                                                        if (
                                                            2 * len(roots)
                                                            < residual_size
                                                        ):
                                                            continue
                                                        support_certificate_count += (
                                                            1
                                                        )
                                                        check_half_height_quotient_shadow(
                                                            roots,
                                                            projective_fiber_directions[
                                                                key
                                                            ],
                                                            "support-fiber",
                                                            key=key,
                                                        )
                                                    if not (
                                                        support_certificate_count
                                                    ):
                                                        raise AssertionError(
                                                            {
                                                                "kind": (
                                                                    "productive-"
                                                                    if productive
                                                                    else ""
                                                                )
                                                                + "marked-core-"
                                                                "deficit-"
                                                                "anchor-"
                                                                "direction-"
                                                                "mds-"
                                                                "projective-"
                                                                "zero-good-"
                                                                "support-"
                                                                "certificate-"
                                                                "failed",
                                                                "p": p,
                                                                "k": k,
                                                                "syndrome": list(
                                                                    syn
                                                                ),
                                                                "fixed_roots": list(
                                                                    fixed_roots
                                                                ),
                                                                "unmarked_core": list(
                                                                    unmarked_core
                                                                ),
                                                                "marked_count": (
                                                                    marked_count
                                                                ),
                                                                "core_deficit": (
                                                                    core_deficit
                                                                ),
                                                                "anchor": list(
                                                                    anchor
                                                                ),
                                                                "candidate": list(
                                                                    candidate
                                                                ),
                                                                "base_roots": list(
                                                                    support_base_roots
                                                                ),
                                                                "fiber_roots": {
                                                                    str(key): list(
                                                                        roots
                                                                    )
                                                                    for (
                                                                        key,
                                                                        roots,
                                                                    ) in (
                                                                        candidate_fiber_roots.items()
                                                                    )
                                                                },
                                                            }
                                                        )
                                            if (
                                                zero_good_candidate_count
                                                > projective_zero_good_envelope_count
                                            ):
                                                raise AssertionError(
                                                    {
                                                        "kind": (
                                                            "productive-"
                                                            if productive
                                                            else ""
                                                        )
                                                        + "marked-core-"
                                                        "deficit-anchor-"
                                                        "direction-mds-"
                                                        "projective-"
                                                        "zero-good-envelope-"
                                                        "failed",
                                                        "p": p,
                                                        "k": k,
                                                        "syndrome": list(syn),
                                                        "fixed_roots": list(
                                                            fixed_roots
                                                        ),
                                                        "unmarked_core": list(
                                                            unmarked_core
                                                        ),
                                                        "marked_count": (
                                                            marked_count
                                                        ),
                                                        "core_deficit": (
                                                            core_deficit
                                                        ),
                                                        "anchor": list(anchor),
                                                        "zero_good_candidates": (
                                                            zero_good_candidate_count
                                                        ),
                                                        "zero_good_envelope": (
                                                            projective_zero_good_envelope_count
                                                        ),
                                                        "base_roots": sorted(
                                                            projective_eval_base_roots
                                                        ),
                                                        "fibers": {
                                                            str(key): sorted(
                                                                roots
                                                            )
                                                            for key, roots in (
                                                                projective_eval_fibers.items()
                                                            )
                                                        },
                                                    }
                                                )
                                            if (
                                                zero_good_candidate_count
                                                > projective_zero_good_incidence_bound
                                            ):
                                                raise AssertionError(
                                                    {
                                                        "kind": (
                                                            "productive-"
                                                            if productive
                                                            else ""
                                                        )
                                                        + "marked-core-"
                                                        "deficit-anchor-"
                                                        "direction-mds-"
                                                        "projective-"
                                                        "zero-good-half-"
                                                        "certificate-incidence-"
                                                        "failed",
                                                        "p": p,
                                                        "k": k,
                                                        "syndrome": list(syn),
                                                        "fixed_roots": list(
                                                            fixed_roots
                                                        ),
                                                        "unmarked_core": list(
                                                            unmarked_core
                                                        ),
                                                        "marked_count": (
                                                            marked_count
                                                        ),
                                                        "core_deficit": (
                                                            core_deficit
                                                        ),
                                                        "anchor": list(anchor),
                                                        "zero_good_candidates": (
                                                            zero_good_candidate_count
                                                        ),
                                                        "half_certificate_size": (
                                                            half_certificate_size
                                                        ),
                                                        "half_certificate_count": (
                                                            projective_half_certificate_count
                                                        ),
                                                        "incidence_bound": (
                                                            projective_zero_good_incidence_bound
                                                        ),
                                                        "base_roots": sorted(
                                                            projective_eval_base_roots
                                                        ),
                                                        "fibers": {
                                                            str(key): sorted(
                                                                roots
                                                            )
                                                            for key, roots in (
                                                                projective_eval_fibers.items()
                                                            )
                                                        },
                                                    }
                                                )
                                            if (
                                                zero_good_candidate_count
                                                > projective_zero_good_local_bound
                                            ):
                                                raise AssertionError(
                                                    projective_local_error(
                                                        "zero-good-local-"
                                                        "incidence-failed",
                                                        zero_good_candidates=(
                                                            zero_good_candidate_count
                                                        ),
                                                        local_bound=(
                                                            projective_zero_good_local_bound
                                                        ),
                                                        base_half_completion_count=(
                                                            base_half_completion_count
                                                        ),
                                                        fiber_half_incidence_bound=(
                                                            fiber_half_incidence_bound
                                                        ),
                                                    )
                                                )
                                            if zero_good_candidate_count:
                                                raise AssertionError(
                                                    projective_local_error(
                                                        "zero-good-candidate-"
                                                        "degree-gap-failed",
                                                        zero_good_candidates=(
                                                            zero_good_candidate_count
                                                        ),
                                                        max_shadow_size=(
                                                            projective_max_direction_shadow_size
                                                        ),
                                                    )
                                                )
                                            split_image_candidates: set[
                                                tuple[int, ...]
                                            ] = set()
                                            split_image_pair_count = 0
                                            for pair in projective_good_pairs:
                                                (
                                                    interpolation_matrix,
                                                    interpolation_coeffs,
                                                    interpolated_locator,
                                                ) = interpolate_good_pair_locator(
                                                    pair
                                                )
                                                pair_locator = cached_locator(
                                                    pair
                                                )
                                                pair_quotient_locator = (
                                                    divide_by_polynomial_exact_mod(
                                                        interpolated_locator,
                                                        pair_locator,
                                                        p,
                                                    )
                                                )
                                                left_row = affine_kernel_row(
                                                    pair[0]
                                                )
                                                right_row = affine_kernel_row(
                                                    pair[1]
                                                )
                                                determinant_scale = (
                                                    left_row[1] * right_row[2]
                                                    - left_row[2] * right_row[1]
                                                ) % p
                                                determinant_p_coeff = (
                                                    left_row[2] * right_row[0]
                                                    - left_row[0] * right_row[2]
                                                ) % p
                                                determinant_q_coeff = (
                                                    left_row[0] * right_row[1]
                                                    - left_row[1] * right_row[0]
                                                ) % p
                                                determinant_locator = tuple(
                                                    (
                                                        determinant_scale
                                                        * residual_locator[index]
                                                        + determinant_p_coeff
                                                        * direction_coeff(
                                                            direction_basis[0],
                                                            index,
                                                        )
                                                        + determinant_q_coeff
                                                        * direction_coeff(
                                                            direction_basis[1],
                                                            index,
                                                        )
                                                    )
                                                    % p
                                                    for index in range(
                                                        residual_size + 1
                                                    )
                                                )
                                                expected_determinant_locator = tuple(
                                                    (
                                                        determinant_scale * coeff
                                                    )
                                                    % p
                                                    for coeff in (
                                                        interpolated_locator
                                                    )
                                                )
                                                if (
                                                    determinant_locator
                                                    != expected_determinant_locator
                                                ):
                                                    raise AssertionError(
                                                        projective_local_error(
                                                            "good-pair-"
                                                            "determinant-"
                                                            "normalization-"
                                                            "failed",
                                                            pair=list(pair),
                                                            determinant=list(
                                                                determinant_locator
                                                            ),
                                                            expected=list(
                                                                expected_determinant_locator
                                                            ),
                                                            scale=(
                                                                determinant_scale
                                                            ),
                                                        )
                                                    )
                                                determinant_quotient = (
                                                    divide_by_polynomial_exact_mod(
                                                        determinant_locator,
                                                        pair_locator,
                                                        p,
                                                    )
                                                )
                                                expected_determinant_quotient = tuple(
                                                    (
                                                        determinant_scale * coeff
                                                    )
                                                    % p
                                                    for coeff in (
                                                        pair_quotient_locator
                                                    )
                                                )
                                                if (
                                                    determinant_quotient
                                                    != expected_determinant_quotient
                                                ):
                                                    raise AssertionError(
                                                        projective_local_error(
                                                            "good-pair-"
                                                            "determinant-"
                                                            "quotient-"
                                                            "normalization-"
                                                            "failed",
                                                            pair=list(pair),
                                                            quotient=list(
                                                                determinant_quotient
                                                            ),
                                                            expected=list(
                                                                expected_determinant_quotient
                                                            ),
                                                            scale=(
                                                                determinant_scale
                                                            ),
                                                        )
                                                    )
                                                reconstructed_from_quotient = (
                                                    multiply_polynomials_mod(
                                                        pair_locator,
                                                        pair_quotient_locator,
                                                        p,
                                                    )
                                                )
                                                if (
                                                    reconstructed_from_quotient
                                                    != interpolated_locator
                                                ):
                                                    raise AssertionError(
                                                        projective_local_error(
                                                            "good-pair-"
                                                            "quotient-"
                                                            "reconstruction-"
                                                            "failed",
                                                            pair=list(pair),
                                                            quotient=list(
                                                                pair_quotient_locator
                                                            ),
                                                            reconstructed=list(
                                                                reconstructed_from_quotient
                                                            ),
                                                            locator=list(
                                                                interpolated_locator
                                                            ),
                                                        )
                                                    )
                                                pair_filtered_sequence = tuple(
                                                    sum(
                                                        pair_locator[offset]
                                                        * filtered_sequence[
                                                            index + offset
                                                        ]
                                                        for offset in range(
                                                            len(pair_locator)
                                                        )
                                                    )
                                                    % p
                                                    for index in range(
                                                        2 * residual_size - 2
                                                    )
                                                )
                                                quotient_vector = hankel_apply(
                                                    pair_filtered_sequence,
                                                    pair_quotient_locator,
                                                    residual_size,
                                                    p,
                                                )
                                                if any(quotient_vector):
                                                    raise AssertionError(
                                                        projective_local_error(
                                                            "good-pair-"
                                                            "quotient-kernel-"
                                                            "failed",
                                                            pair=list(pair),
                                                            quotient=list(
                                                                pair_quotient_locator
                                                            ),
                                                            quotient_vector=list(
                                                                quotient_vector
                                                            ),
                                                        )
                                                    )
                                                interpolated_vector = hankel_apply(
                                                    filtered_sequence,
                                                    interpolated_locator,
                                                    residual_size,
                                                    p,
                                                )
                                                if any(interpolated_vector):
                                                    raise AssertionError(
                                                        projective_local_error(
                                                            "good-pair-image-"
                                                            "kernel-failed",
                                                            pair=list(pair),
                                                            matrix=[
                                                                list(row)
                                                                for row in (
                                                                    interpolation_matrix
                                                                )
                                                            ],
                                                            coeffs=list(
                                                                interpolation_coeffs
                                                            ),
                                                            locator=list(
                                                                interpolated_locator
                                                            ),
                                                            hankel_vector=list(
                                                                interpolated_vector
                                                            ),
                                                        )
                                                    )
                                                split_roots = tuple(
                                                    root
                                                    for root in available_roots
                                                    if not polynomial_eval_mod(
                                                        interpolated_locator,
                                                        domain[root],
                                                        p,
                                                    )
                                                )
                                                quotient_roots = tuple(
                                                    root
                                                    for root in available_roots
                                                    if root not in pair
                                                    and not polynomial_eval_mod(
                                                        pair_quotient_locator,
                                                        domain[root],
                                                        p,
                                                    )
                                                )
                                                determinant_gate_roots = tuple(
                                                    root
                                                    for root in available_roots
                                                    if root not in pair
                                                    and not determinant_mod(
                                                        (
                                                            affine_kernel_row(
                                                                pair[0]
                                                            ),
                                                            affine_kernel_row(
                                                                pair[1]
                                                            ),
                                                            affine_kernel_row(
                                                                root
                                                            ),
                                                        ),
                                                        p,
                                                    )
                                                )
                                                if (
                                                    determinant_gate_roots
                                                    != quotient_roots
                                                ):
                                                    raise AssertionError(
                                                        projective_local_error(
                                                            "good-pair-"
                                                            "determinant-"
                                                            "gate-failed",
                                                            pair=list(pair),
                                                            determinant_roots=list(
                                                                determinant_gate_roots
                                                            ),
                                                            quotient_roots=list(
                                                                quotient_roots
                                                            ),
                                                        )
                                                    )
                                                split_candidate = (
                                                    len(split_roots)
                                                    == residual_size
                                                    and cached_locator(
                                                        split_roots
                                                    )
                                                    == interpolated_locator
                                                )
                                                quotient_split_candidate = (
                                                    len(quotient_roots)
                                                    == residual_size - 2
                                                    and cached_locator(
                                                        quotient_roots
                                                    )
                                                    == pair_quotient_locator
                                                )
                                                if (
                                                    split_candidate
                                                    != quotient_split_candidate
                                                ):
                                                    raise AssertionError(
                                                        projective_local_error(
                                                            "good-pair-"
                                                            "quotient-split-"
                                                            "equivalence-"
                                                            "failed",
                                                            pair=list(pair),
                                                            split_roots=list(
                                                                split_roots
                                                            ),
                                                            quotient_roots=list(
                                                                quotient_roots
                                                            ),
                                                            locator=list(
                                                                interpolated_locator
                                                            ),
                                                            quotient=list(
                                                                pair_quotient_locator
                                                            ),
                                                        )
                                                    )
                                                if split_candidate and tuple(
                                                    sorted((*pair, *quotient_roots))
                                                ) != split_roots:
                                                    raise AssertionError(
                                                        projective_local_error(
                                                            "good-pair-"
                                                            "quotient-roots-"
                                                            "failed",
                                                            pair=list(pair),
                                                            split_roots=list(
                                                                split_roots
                                                            ),
                                                            quotient_roots=list(
                                                                quotient_roots
                                                            ),
                                                        )
                                                    )
                                                owner = pair_owner.get(pair)
                                                if split_candidate:
                                                    split_image_pair_count += 1
                                                    split_image_candidates.add(
                                                        split_roots
                                                    )
                                                    if (
                                                        split_roots
                                                        not in residual_candidate_set
                                                    ):
                                                        raise AssertionError(
                                                            projective_local_error(
                                                                "good-pair-"
                                                                "split-image-"
                                                                "missing-"
                                                                "candidate",
                                                                pair=list(pair),
                                                                split_roots=list(
                                                                    split_roots
                                                                ),
                                                                locator=list(
                                                                    interpolated_locator
                                                                ),
                                                            )
                                                        )
                                                    if owner != split_roots:
                                                        raise AssertionError(
                                                            projective_local_error(
                                                                "good-pair-"
                                                                "split-image-"
                                                                "owner-"
                                                                "failed",
                                                                pair=list(pair),
                                                                split_roots=list(
                                                                    split_roots
                                                                ),
                                                                owner=(
                                                                    list(owner)
                                                                    if owner
                                                                    is not None
                                                                    else None
                                                                ),
                                                            )
                                                        )
                                                elif owner is not None:
                                                    raise AssertionError(
                                                        projective_local_error(
                                                            "good-pair-owned-"
                                                            "image-nonsplit-"
                                                            "failed",
                                                            pair=list(pair),
                                                            owner=list(owner),
                                                            split_roots=list(
                                                                split_roots
                                                            ),
                                                            locator=list(
                                                                interpolated_locator
                                                            ),
                                                        )
                                                    )
                                            if (
                                                split_image_candidates
                                                != residual_candidate_set
                                            ):
                                                raise AssertionError(
                                                    projective_local_error(
                                                        "good-pair-split-"
                                                        "image-surjectivity-"
                                                        "failed",
                                                        image=[
                                                            list(candidate)
                                                            for candidate in sorted(
                                                                split_image_candidates
                                                            )
                                                        ],
                                                        candidates=[
                                                            list(candidate)
                                                            for candidate in sorted(
                                                                residual_candidate_set
                                                            )
                                                        ],
                                                    )
                                                )
                                            if split_image_pair_count != len(
                                                pair_owner
                                            ):
                                                raise AssertionError(
                                                    projective_local_error(
                                                        "good-pair-split-"
                                                        "image-count-failed",
                                                        split_image_pair_count=(
                                                            split_image_pair_count
                                                        ),
                                                        owned_pair_count=len(
                                                            pair_owner
                                                        ),
                                                    )
                                                )
                                            image_fiber_counts = Counter(
                                                pair_owner.values()
                                            )
                                            if (
                                                dict(image_fiber_counts)
                                                != candidate_good_pair_counts
                                            ):
                                                raise AssertionError(
                                                    projective_local_error(
                                                        "good-pair-image-"
                                                        "fiber-count-failed",
                                                        image_fibers={
                                                            str(candidate): count
                                                            for (
                                                                candidate,
                                                                count,
                                                            ) in sorted(
                                                                image_fiber_counts.items()
                                                            )
                                                        },
                                                        candidate_good_pairs={
                                                            str(candidate): count
                                                            for (
                                                                candidate,
                                                                count,
                                                            ) in sorted(
                                                                candidate_good_pair_counts.items()
                                                            )
                                                        },
                                                    )
                                                )
                                            if (
                                                sum(
                                                    candidate_good_pair_counts.values()
                                                )
                                                != len(pair_owner)
                                            ):
                                                raise AssertionError(
                                                    projective_local_error(
                                                        "good-pair-image-"
                                                        "weighted-count-failed",
                                                        good_pair_sum=sum(
                                                            candidate_good_pair_counts.values()
                                                        ),
                                                        owned_pair_count=len(
                                                            pair_owner
                                                        ),
                                                    )
                                                )
                                            projective_zero_good_closure_bound = (
                                                len(projective_good_pairs)
                                                + projective_zero_good_envelope_count
                                            )
                                            projective_half_certificate_closure_bound = (
                                                len(projective_good_pairs)
                                                + projective_zero_good_incidence_bound
                                            )
                                            projective_local_half_certificate_closure_bound = (
                                                len(projective_good_pairs)
                                                + projective_zero_good_local_bound
                                            )
                                            projective_degree_gap_closure_bound = len(
                                                projective_good_pairs
                                            )
                                            if (
                                                len(residual_candidates)
                                                > projective_zero_good_closure_bound
                                            ):
                                                raise AssertionError(
                                                    {
                                                        "kind": (
                                                            "productive-"
                                                            if productive
                                                            else ""
                                                        )
                                                        + "marked-core-"
                                                        "deficit-anchor-"
                                                        "direction-mds-"
                                                        "projective-"
                                                        "zero-good-closure-"
                                                        "bound-failed",
                                                        "p": p,
                                                        "k": k,
                                                        "syndrome": list(syn),
                                                        "fixed_roots": list(
                                                            fixed_roots
                                                        ),
                                                        "unmarked_core": list(
                                                            unmarked_core
                                                        ),
                                                        "marked_count": (
                                                            marked_count
                                                        ),
                                                        "core_deficit": (
                                                            core_deficit
                                                        ),
                                                        "anchor": list(anchor),
                                                        "residual_candidates": (
                                                            len(
                                                                residual_candidates
                                                            )
                                                        ),
                                                        "good_pair_count": (
                                                            len(
                                                                projective_good_pairs
                                                            )
                                                        ),
                                                        "zero_good_envelope": (
                                                            projective_zero_good_envelope_count
                                                        ),
                                                        "bound": (
                                                            projective_zero_good_closure_bound
                                                        ),
                                                    }
                                                )
                                            if (
                                                len(residual_candidates)
                                                > projective_degree_gap_closure_bound
                                            ):
                                                raise AssertionError(
                                                    projective_local_error(
                                                        "degree-gap-closure-"
                                                        "bound-failed",
                                                        residual_candidates=(
                                                            len(
                                                                residual_candidates
                                                            )
                                                        ),
                                                        good_pair_count=(
                                                            projective_degree_gap_closure_bound
                                                        ),
                                                        max_shadow_size=(
                                                            projective_max_direction_shadow_size
                                                        ),
                                                    )
                                                )
                                            if (
                                                len(residual_candidates)
                                                > projective_half_certificate_closure_bound
                                            ):
                                                raise AssertionError(
                                                    {
                                                        "kind": (
                                                            "productive-"
                                                            if productive
                                                            else ""
                                                        )
                                                        + "marked-core-"
                                                        "deficit-anchor-"
                                                        "direction-mds-"
                                                        "projective-"
                                                        "half-certificate-"
                                                        "closure-bound-failed",
                                                        "p": p,
                                                        "k": k,
                                                        "syndrome": list(syn),
                                                        "fixed_roots": list(
                                                            fixed_roots
                                                        ),
                                                        "unmarked_core": list(
                                                            unmarked_core
                                                        ),
                                                        "marked_count": (
                                                            marked_count
                                                        ),
                                                        "core_deficit": (
                                                            core_deficit
                                                        ),
                                                        "anchor": list(anchor),
                                                        "residual_candidates": (
                                                            len(
                                                                residual_candidates
                                                            )
                                                        ),
                                                        "good_pair_count": (
                                                            len(
                                                                projective_good_pairs
                                                            )
                                                        ),
                                                        "half_certificate_size": (
                                                            half_certificate_size
                                                        ),
                                                        "half_certificate_count": (
                                                            projective_half_certificate_count
                                                        ),
                                                        "incidence_bound": (
                                                            projective_zero_good_incidence_bound
                                                        ),
                                                        "bound": (
                                                            projective_half_certificate_closure_bound
                                                        ),
                                                    }
                                                )
                                            if (
                                                len(residual_candidates)
                                                > projective_local_half_certificate_closure_bound
                                            ):
                                                raise AssertionError(
                                                    projective_local_error(
                                                        "local-half-"
                                                        "certificate-closure-"
                                                        "bound-failed",
                                                        residual_candidates=(
                                                            len(
                                                                residual_candidates
                                                            )
                                                        ),
                                                        good_pair_count=len(
                                                            projective_good_pairs
                                                        ),
                                                        local_bound=(
                                                            projective_zero_good_local_bound
                                                        ),
                                                        bound=(
                                                            projective_local_half_certificate_closure_bound
                                                        ),
                                                    )
                                                )
                                            if residual_candidates:
                                                nonbase_lower_count = (
                                                    residual_size
                                                    - candidate_base_occupancy_max
                                                )
                                                concentration_good_pair_lower = (
                                                    math.comb(
                                                        nonbase_lower_count,
                                                        2,
                                                    )
                                                    - capped_pair_cluster_bound(
                                                        nonbase_lower_count,
                                                        candidate_fiber_occupancy_max,
                                                    )
                                                )
                                                if (
                                                    candidate_good_pair_min
                                                    is not None
                                                    and candidate_good_pair_min
                                                    < concentration_good_pair_lower
                                                ):
                                                    raise AssertionError(
                                                        {
                                                            "kind": (
                                                                "productive-"
                                                                if productive
                                                                else ""
                                                            )
                                                            + "marked-core-"
                                                            "deficit-anchor-"
                                                            "direction-mds-"
                                                            "projective-"
                                                            "concentration-"
                                                            "lower-bound-"
                                                            "failed",
                                                            "p": p,
                                                            "k": k,
                                                            "syndrome": list(syn),
                                                            "fixed_roots": list(
                                                                fixed_roots
                                                            ),
                                                            "unmarked_core": list(
                                                                unmarked_core
                                                            ),
                                                            "marked_count": (
                                                                marked_count
                                                            ),
                                                            "core_deficit": (
                                                                core_deficit
                                                            ),
                                                            "anchor": list(anchor),
                                                            "candidate_good_pair_min": (
                                                                candidate_good_pair_min
                                                            ),
                                                            "base_occupancy_max": (
                                                                candidate_base_occupancy_max
                                                            ),
                                                            "fiber_occupancy_max": (
                                                                candidate_fiber_occupancy_max
                                                            ),
                                                            "lower_bound": (
                                                                concentration_good_pair_lower
                                                            ),
                                                        }
                                                    )
                                                slice_height_good_pair_lower = (
                                                    b2_good_pair_lower_from_slice_height(
                                                        residual_size,
                                                        projective_root_shadow_height,
                                                    )
                                                )
                                                if (
                                                    candidate_good_pair_min
                                                    is not None
                                                    and candidate_good_pair_min
                                                    < slice_height_good_pair_lower
                                                ):
                                                    raise AssertionError(
                                                        {
                                                            "kind": (
                                                                "productive-"
                                                                if productive
                                                                else ""
                                                            )
                                                            + "marked-core-"
                                                            "deficit-anchor-"
                                                            "direction-mds-"
                                                            "projective-"
                                                            "slice-height-"
                                                            "lower-bound-"
                                                            "failed",
                                                            "p": p,
                                                            "k": k,
                                                            "syndrome": list(syn),
                                                            "fixed_roots": list(
                                                                fixed_roots
                                                            ),
                                                            "unmarked_core": list(
                                                                unmarked_core
                                                            ),
                                                            "marked_count": (
                                                                marked_count
                                                            ),
                                                            "core_deficit": (
                                                                core_deficit
                                                            ),
                                                            "anchor": list(anchor),
                                                            "candidate_good_pair_min": (
                                                                candidate_good_pair_min
                                                            ),
                                                            "root_shadow_height": (
                                                                projective_root_shadow_height
                                                            ),
                                                            "lower_bound": (
                                                                slice_height_good_pair_lower
                                                            ),
                                                        }
                                                    )
                                                if (
                                                    slice_height_good_pair_lower
                                                    and len(residual_candidates)
                                                    > len(projective_good_pairs)
                                                    // slice_height_good_pair_lower
                                                ):
                                                    raise AssertionError(
                                                        {
                                                            "kind": (
                                                                "productive-"
                                                                if productive
                                                                else ""
                                                            )
                                                            + "marked-core-"
                                                            "deficit-anchor-"
                                                            "direction-mds-"
                                                            "projective-"
                                                            "slice-height-"
                                                            "bound-failed",
                                                            "p": p,
                                                            "k": k,
                                                            "syndrome": list(syn),
                                                            "fixed_roots": list(
                                                                fixed_roots
                                                            ),
                                                            "unmarked_core": list(
                                                                unmarked_core
                                                            ),
                                                            "marked_count": (
                                                                marked_count
                                                            ),
                                                            "core_deficit": (
                                                                core_deficit
                                                            ),
                                                            "anchor": list(anchor),
                                                            "residual_candidates": (
                                                                len(
                                                                    residual_candidates
                                                                )
                                                            ),
                                                            "good_pair_count": (
                                                                len(
                                                                    projective_good_pairs
                                                                )
                                                            ),
                                                            "root_shadow_height": (
                                                                projective_root_shadow_height
                                                            ),
                                                            "lower_bound": (
                                                                slice_height_good_pair_lower
                                                            ),
                                                        }
                                                    )
                                            if (
                                                candidate_good_pair_min
                                                and len(residual_candidates)
                                                > len(projective_good_pairs)
                                                // candidate_good_pair_min
                                            ):
                                                raise AssertionError(
                                                    {
                                                        "kind": (
                                                            "productive-"
                                                            if productive
                                                            else ""
                                                        )
                                                        + "marked-core-"
                                                        "deficit-anchor-"
                                                        "direction-mds-"
                                                        "projective-good-pair-"
                                                        "bound-failed",
                                                        "p": p,
                                                        "k": k,
                                                        "syndrome": list(syn),
                                                        "fixed_roots": list(
                                                            fixed_roots
                                                        ),
                                                        "unmarked_core": list(
                                                            unmarked_core
                                                        ),
                                                        "marked_count": (
                                                            marked_count
                                                        ),
                                                        "core_deficit": (
                                                            core_deficit
                                                        ),
                                                        "anchor": list(anchor),
                                                        "candidate_count": len(
                                                            residual_candidates
                                                        ),
                                                        "good_pair_count": len(
                                                            projective_good_pairs
                                                        ),
                                                        "candidate_good_pair_min": (
                                                            candidate_good_pair_min
                                                        ),
                                                    }
                                                )
                                        if not root_slice_persistent:
                                            finite_root_slice_bound = (
                                                binomial_or_zero(
                                                    residual_size - 1,
                                                    residual_direction_dim,
                                                )
                                            )
                                            if (
                                                len(bad_direction_subsets)
                                                > finite_root_slice_bound
                                            ):
                                                raise AssertionError(
                                                    {
                                                        "kind": (
                                                            "productive-"
                                                            if productive
                                                            else ""
                                                        )
                                                        + "marked-core-"
                                                        "deficit-anchor-"
                                                        "direction-mds-"
                                                        "finite-root-slice-"
                                                        "bound-failed",
                                                        "p": p,
                                                        "k": k,
                                                        "syndrome": list(syn),
                                                        "fixed_roots": list(
                                                            fixed_roots
                                                        ),
                                                        "unmarked_core": list(
                                                            unmarked_core
                                                        ),
                                                        "marked_count": (
                                                            marked_count
                                                        ),
                                                        "core_deficit": (
                                                            core_deficit
                                                        ),
                                                        "anchor": list(anchor),
                                                        "direction_dim": (
                                                            residual_direction_dim
                                                        ),
                                                        "bad_subset_count": len(
                                                            bad_direction_subsets
                                                        ),
                                                        "bound": (
                                                            finite_root_slice_bound
                                                        ),
                                                        "root_slice_bad_roots": (
                                                            sorted(
                                                                root_slice_bad_roots
                                                            )
                                                        ),
                                                    }
                                                )
                                        for left, right in itertools.combinations(
                                            residual_candidates,
                                            2,
                                        ):
                                            shared_roots = sorted(
                                                set(left) & set(right)
                                            )
                                            for subset in itertools.combinations(
                                                shared_roots,
                                                residual_direction_dim,
                                            ):
                                                if (
                                                    subset
                                                    not in bad_direction_subsets
                                                ):
                                                    raise AssertionError(
                                                        {
                                                            "kind": (
                                                                "productive-"
                                                                if productive
                                                                else ""
                                                            )
                                                            + "marked-core-"
                                                            "deficit-anchor-"
                                                            "direction-mds-"
                                                            "collision-failed",
                                                            "p": p,
                                                            "k": k,
                                                            "syndrome": list(syn),
                                                            "fixed_roots": list(
                                                                fixed_roots
                                                            ),
                                                            "unmarked_core": list(
                                                                unmarked_core
                                                            ),
                                                            "marked_count": (
                                                                marked_count
                                                            ),
                                                            "core_deficit": (
                                                                core_deficit
                                                            ),
                                                            "anchor": list(anchor),
                                                            "direction_dim": (
                                                                residual_direction_dim
                                                            ),
                                                            "left": list(left),
                                                            "right": list(right),
                                                            "subset": list(subset),
                                                            "bad_subsets": [
                                                                list(item)
                                                                for item in sorted(
                                                                    bad_direction_subsets
                                                                )
                                                            ],
                                                        }
                                                    )
                                        bad_subset_count = len(
                                            bad_direction_subsets
                                        )
                                        numerator = (
                                            math.comb(
                                                len(available_roots),
                                                residual_direction_dim,
                                            )
                                            - bad_subset_count
                                            + bad_subset_count
                                            * math.comb(
                                                (
                                                    len(available_roots)
                                                    - residual_direction_dim
                                                ),
                                                (
                                                    residual_size
                                                    - residual_direction_dim
                                                ),
                                            )
                                        )
                                        direction_mds_bound = numerator // math.comb(
                                            residual_size,
                                            residual_direction_dim,
                                        )
                                        deficit_anchor_direction_mds_checks += 1
                                        deficit_anchor_direction_mds_bad_subsets += (
                                            bad_subset_count
                                        )
                                        deficit_anchor_direction_mds_max_bad_subsets = max(
                                            deficit_anchor_direction_mds_max_bad_subsets,
                                            bad_subset_count,
                                        )
                                        deficit_anchor_direction_mds_max_bound = max(
                                            deficit_anchor_direction_mds_max_bound,
                                            direction_mds_bound,
                                        )
                                        if (
                                            len(residual_candidates)
                                            > direction_mds_bound
                                        ):
                                            raise AssertionError(
                                                {
                                                    "kind": (
                                                        "productive-"
                                                        if productive
                                                        else ""
                                                    )
                                                    + "marked-core-deficit-"
                                                    "anchor-direction-mds-bound-"
                                                    "failed",
                                                    "p": p,
                                                    "k": k,
                                                    "syndrome": list(syn),
                                                    "fixed_roots": list(
                                                        fixed_roots
                                                    ),
                                                    "unmarked_core": list(
                                                        unmarked_core
                                                    ),
                                                    "marked_count": marked_count,
                                                    "core_deficit": core_deficit,
                                                    "anchor": list(anchor),
                                                    "direction_dim": (
                                                        residual_direction_dim
                                                    ),
                                                    "bad_subset_count": (
                                                        bad_subset_count
                                                    ),
                                                    "candidate_count": len(
                                                        residual_candidates
                                                    ),
                                                    "bound": direction_mds_bound,
                                                }
                                            )
                                    residual_bound = sum(
                                        math.comb(len(available_roots), size)
                                        for size in range(
                                            residual_direction_dim + 1
                                        )
                                    )
                                    deficit_anchor_residual_fiber_checks += 1
                                    deficit_anchor_residual_fiber_labels += (
                                        len(residual_candidates)
                                    )
                                    deficit_anchor_residual_fiber_max_size = max(
                                        deficit_anchor_residual_fiber_max_size,
                                        len(residual_candidates),
                                    )
                                    deficit_anchor_residual_fiber_max_direction = max(
                                        deficit_anchor_residual_fiber_max_direction,
                                        residual_direction_dim,
                                    )
                                    if len(residual_candidates) > residual_bound:
                                        raise AssertionError(
                                            {
                                                "kind": (
                                                    "productive-"
                                                    if productive
                                                    else ""
                                                )
                                                + "marked-core-deficit-"
                                                "anchor-residual-bound-"
                                                "failed",
                                                "p": p,
                                                "k": k,
                                                "syndrome": list(syn),
                                                "fixed_roots": list(
                                                    fixed_roots
                                                ),
                                                "unmarked_core": list(
                                                    unmarked_core
                                                ),
                                                "marked_count": marked_count,
                                                "core_deficit": core_deficit,
                                                "anchor": list(anchor),
                                                "direction_dim": (
                                                    residual_direction_dim
                                                ),
                                                "candidate_count": len(
                                                    residual_candidates
                                                ),
                                                "bound": residual_bound,
                                                "candidates": [
                                                    list(candidate)
                                                    for candidate in (
                                                        residual_candidates
                                                    )
                                                ],
                                            }
                                        )
                        if len(anchor_to_support) != packed_subsets:
                            raise AssertionError(
                                {
                                    "kind": (
                                        "productive-"
                                        if productive
                                        else ""
                                    )
                                    + "marked-core-deficit-anchor-"
                                    "count-failed",
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "fixed_roots": list(fixed_roots),
                                    "unmarked_core": list(unmarked_core),
                                    "marked_count": marked_count,
                                    "core_deficit": core_deficit,
                                    "anchor_count": len(
                                        anchor_to_support
                                    ),
                                    "expected": packed_subsets,
                                }
                            )
                        available_subsets = math.comb(
                            n - len(unmarked_core),
                            core_deficit,
                        )
                        if packed_subsets > available_subsets:
                            raise AssertionError(
                                {
                                    "kind": (
                                        "productive-"
                                        if productive
                                        else ""
                                    )
                                    + "marked-core-deficit-packing-"
                                    "bound-failed",
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "fixed_roots": list(fixed_roots),
                                    "unmarked_core": list(unmarked_core),
                                    "marked_count": marked_count,
                                    "core_deficit": core_deficit,
                                    "fiber_size": fiber_size,
                                    "packed_subsets": packed_subsets,
                                    "available_subsets": available_subsets,
                                }
                            )
                    if marked_count <= t and fiber_size > 1:
                        raise AssertionError(
                            {
                                "kind": (
                                    "productive-"
                                    if productive
                                    else ""
                                )
                                + "marked-core-fiber-uniqueness-"
                                "failed",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "unmarked_core": list(unmarked_core),
                                "marked_count": marked_count,
                                "supports": [
                                    list(support)
                                    for support in unique_supports
                                ],
                            }
                        )
                    if marked_count == t + 1:
                        if unmarked_core:
                            nonempty_boundary_checks += 1
                            nonempty_boundary_max_size = max(
                                nonempty_boundary_max_size,
                                fiber_size,
                            )
                            if fiber_size > 1:
                                raise AssertionError(
                                    {
                                        "kind": (
                                            "productive-"
                                            if productive
                                            else ""
                                        )
                                        + "marked-core-nonempty-"
                                        "boundary-uniqueness-failed",
                                        "p": p,
                                        "k": k,
                                        "syndrome": list(syn),
                                        "fixed_roots": list(fixed_roots),
                                        "unmarked_core": list(
                                            unmarked_core
                                        ),
                                        "marked_count": marked_count,
                                        "supports": [
                                            list(support)
                                            for support in unique_supports
                                        ],
                                    }
                                )
                        else:
                            empty_boundary_checks += 1
                            empty_boundary_labels += fiber_size
                            empty_boundary_max_size = max(
                                empty_boundary_max_size,
                                fiber_size,
                            )
                            root_linear_supports: set[tuple[int, ...]] = set()
                            if n == 2 * marked_count:
                                for support in unique_supports:
                                    support_scalars = (
                                        marked_roots_for_split_support(
                                            support
                                        )
                                    )
                                    amplitudes = {}
                                    for root_index in support:
                                        root = domain[root_index]
                                        denominator = 1
                                        for other_root_index in support:
                                            if other_root_index == root_index:
                                                continue
                                            denominator = (
                                                denominator
                                                * (
                                                    root
                                                    - domain[other_root_index]
                                                )
                                            ) % p
                                        amplitudes[root_index] = (
                                            support_scalars[root_index]
                                            * pow(denominator, -1, p)
                                        ) % p
                                    root_linear_values = {
                                        amplitude
                                        * pow(domain[root_index], -1, p)
                                        % p
                                        for root_index, amplitude in (
                                            amplitudes.items()
                                        )
                                    }
                                    root_linear = (
                                        len(root_linear_values) == 1
                                        and 0 not in root_linear_values
                                    )
                                    empty_boundary_root_linear_checks += 1
                                    if root_linear:
                                        empty_boundary_root_linear_hits += 1
                                        root_linear_supports.add(support)
                                if fiber_size > 1:
                                    for left, right in itertools.combinations(
                                        unique_supports,
                                        2,
                                    ):
                                        empty_boundary_complement_pair_checks += 1
                                        if (
                                            set(left) | set(right)
                                            != set(range(n))
                                            or set(left) & set(right)
                                            or left not in root_linear_supports
                                            or right not in root_linear_supports
                                        ):
                                            raise AssertionError(
                                                {
                                                    "kind": (
                                                        "productive-"
                                                        if productive
                                                        else ""
                                                    )
                                                    + "empty-core-boundary-"
                                                    "non-root-linear-"
                                                    "complement-pair",
                                                    "p": p,
                                                    "k": k,
                                                    "syndrome": list(syn),
                                                    "fixed_roots": list(
                                                        fixed_roots
                                                    ),
                                                    "marked_count": (
                                                        marked_count
                                                    ),
                                                    "left_support": list(left),
                                                    "right_support": list(
                                                        right
                                                    ),
                                                    "root_linear_supports": [
                                                        list(support)
                                                        for support in sorted(
                                                            root_linear_supports
                                                        )
                                                    ],
                                                }
                                            )
                        for left, right in itertools.combinations(
                            unique_supports,
                            2,
                        ):
                            if set(left) & set(right):
                                raise AssertionError(
                                    {
                                        "kind": (
                                            "productive-"
                                            if productive
                                            else ""
                                        )
                                        + "marked-core-boundary-"
                                        "overlapping-fiber",
                                        "p": p,
                                        "k": k,
                                        "syndrome": list(syn),
                                        "fixed_roots": list(fixed_roots),
                                        "unmarked_core": list(
                                            unmarked_core
                                        ),
                                        "marked_count": marked_count,
                                        "left_support": list(left),
                                        "right_support": list(right),
                                    }
                                )
                        matching_bound = (
                            n - len(unmarked_core)
                        ) // marked_count
                        if fiber_size > matching_bound:
                            raise AssertionError(
                                {
                                    "kind": (
                                        "productive-"
                                        if productive
                                        else ""
                                    )
                                    + "marked-core-boundary-"
                                    "matching-bound-failed",
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "fixed_roots": list(fixed_roots),
                                    "unmarked_core": list(unmarked_core),
                                    "marked_count": marked_count,
                                    "fiber_size": fiber_size,
                                    "matching_bound": matching_bound,
                                }
                            )
                return (
                    fiber_checks,
                    fiber_labels,
                    max_fiber_size,
                    nonempty_boundary_checks,
                    nonempty_boundary_max_size,
                    empty_boundary_checks,
                    empty_boundary_labels,
                    empty_boundary_max_size,
                    empty_boundary_root_linear_checks,
                    empty_boundary_root_linear_hits,
                    empty_boundary_complement_pair_checks,
                    moment_complete_checks,
                    moment_complete_max_size,
                    deficit_packing_checks,
                    deficit_packing_max_deficit,
                    deficit_packing_max_size,
                    deficit_anchor_label_checks,
                    deficit_anchor_max_labels,
                    deficit_anchor_kernel_checks,
                    deficit_anchor_max_residual_size,
                    deficit_anchor_residual_fiber_checks,
                    deficit_anchor_residual_fiber_labels,
                    deficit_anchor_residual_fiber_max_size,
                    deficit_anchor_residual_fiber_max_direction,
                    deficit_anchor_line_kernel_checks,
                    deficit_anchor_line_kernel_max_direction_roots,
                    deficit_anchor_line_kernel_max_sharp_bound,
                    deficit_anchor_direction_mds_checks,
                    deficit_anchor_direction_mds_bad_subsets,
                    deficit_anchor_direction_mds_max_bad_subsets,
                    deficit_anchor_direction_mds_max_bound,
                    deficit_anchor_root_slice_checks,
                    deficit_anchor_root_slice_labels,
                    deficit_anchor_root_slice_bad_labels,
                    deficit_anchor_root_slice_max_bad_per_anchor,
                    deficit_anchor_endpoint_rank_checks,
                    deficit_anchor_endpoint_rank_defects,
                    deficit_anchor_endpoint_rank_max_defect,
                )

            (
                marked_core_fiber_checks,
                marked_core_fiber_labels,
                marked_core_fiber_max_size,
                marked_core_nonempty_boundary_checks,
                marked_core_nonempty_boundary_max_size,
                empty_core_boundary_fiber_checks,
                empty_core_boundary_fiber_labels,
                empty_core_boundary_fiber_max_size,
                empty_core_boundary_root_linear_checks,
                empty_core_boundary_root_linear_hits,
                empty_core_boundary_complement_pair_checks,
                moment_complete_core_checks,
                moment_complete_core_max_fiber_size,
                deficit_packing_core_checks,
                deficit_packing_core_max_deficit,
                deficit_packing_core_max_fiber_size,
                deficit_anchor_label_checks,
                deficit_anchor_max_labels_per_fiber,
                deficit_anchor_kernel_checks,
                deficit_anchor_max_residual_size,
                deficit_anchor_residual_fiber_checks,
                deficit_anchor_residual_fiber_labels,
                deficit_anchor_residual_fiber_max_size,
                deficit_anchor_residual_fiber_max_direction,
                deficit_anchor_line_kernel_checks,
                deficit_anchor_line_kernel_max_direction_roots,
                deficit_anchor_line_kernel_max_sharp_bound,
                deficit_anchor_direction_mds_checks,
                deficit_anchor_direction_mds_bad_subsets,
                deficit_anchor_direction_mds_max_bad_subsets,
                deficit_anchor_direction_mds_max_bound,
                deficit_anchor_root_slice_checks,
                deficit_anchor_root_slice_labels,
                deficit_anchor_root_slice_bad_labels,
                deficit_anchor_root_slice_max_bad_per_anchor,
                deficit_anchor_endpoint_rank_checks,
                deficit_anchor_endpoint_rank_defects,
                deficit_anchor_endpoint_rank_max_defect,
            ) = audit_marked_core_fibers(
                total_split_supports,
                productive=False,
            )
            (
                productive_marked_core_fiber_checks,
                productive_marked_core_fiber_labels,
                productive_marked_core_fiber_max_size,
                productive_marked_core_nonempty_boundary_checks,
                productive_marked_core_nonempty_boundary_max_size,
                productive_empty_core_boundary_fiber_checks,
                productive_empty_core_boundary_fiber_labels,
                productive_empty_core_boundary_fiber_max_size,
                productive_empty_core_boundary_root_linear_checks,
                productive_empty_core_boundary_root_linear_hits,
                productive_empty_core_boundary_complement_pair_checks,
                productive_moment_complete_core_checks,
                productive_moment_complete_core_max_fiber_size,
                productive_deficit_packing_core_checks,
                productive_deficit_packing_core_max_deficit,
                productive_deficit_packing_core_max_fiber_size,
                productive_deficit_anchor_label_checks,
                productive_deficit_anchor_max_labels_per_fiber,
                productive_deficit_anchor_kernel_checks,
                productive_deficit_anchor_max_residual_size,
                productive_deficit_anchor_residual_fiber_checks,
                productive_deficit_anchor_residual_fiber_labels,
                productive_deficit_anchor_residual_fiber_max_size,
                productive_deficit_anchor_residual_fiber_max_direction,
                productive_deficit_anchor_line_kernel_checks,
                productive_deficit_anchor_line_kernel_max_direction_roots,
                productive_deficit_anchor_line_kernel_max_sharp_bound,
                productive_deficit_anchor_direction_mds_checks,
                productive_deficit_anchor_direction_mds_bad_subsets,
                productive_deficit_anchor_direction_mds_max_bad_subsets,
                productive_deficit_anchor_direction_mds_max_bound,
                productive_deficit_anchor_root_slice_checks,
                productive_deficit_anchor_root_slice_labels,
                productive_deficit_anchor_root_slice_bad_labels,
                productive_deficit_anchor_root_slice_max_bad_per_anchor,
                productive_deficit_anchor_endpoint_rank_checks,
                productive_deficit_anchor_endpoint_rank_defects,
                productive_deficit_anchor_endpoint_rank_max_defect,
            ) = audit_marked_core_fibers(
                productive_total_split_supports,
                productive=True,
            )
            terminal_tree_marked_core_fiber_checks += (
                marked_core_fiber_checks
            )
            terminal_tree_productive_marked_core_fiber_checks += (
                productive_marked_core_fiber_checks
            )
            terminal_tree_marked_core_fiber_labels += (
                marked_core_fiber_labels
            )
            terminal_tree_productive_marked_core_fiber_labels += (
                productive_marked_core_fiber_labels
            )
            terminal_tree_marked_core_fiber_max_size = max(
                terminal_tree_marked_core_fiber_max_size,
                marked_core_fiber_max_size,
            )
            terminal_tree_productive_marked_core_fiber_max_size = max(
                terminal_tree_productive_marked_core_fiber_max_size,
                productive_marked_core_fiber_max_size,
            )
            terminal_tree_marked_core_nonempty_boundary_checks += (
                marked_core_nonempty_boundary_checks
            )
            terminal_tree_productive_marked_core_nonempty_boundary_checks += (
                productive_marked_core_nonempty_boundary_checks
            )
            terminal_tree_marked_core_nonempty_boundary_max_size = max(
                terminal_tree_marked_core_nonempty_boundary_max_size,
                marked_core_nonempty_boundary_max_size,
            )
            terminal_tree_productive_marked_core_nonempty_boundary_max_size = max(
                terminal_tree_productive_marked_core_nonempty_boundary_max_size,
                productive_marked_core_nonempty_boundary_max_size,
            )
            terminal_tree_empty_core_boundary_fiber_checks += (
                empty_core_boundary_fiber_checks
            )
            terminal_tree_productive_empty_core_boundary_fiber_checks += (
                productive_empty_core_boundary_fiber_checks
            )
            terminal_tree_empty_core_boundary_fiber_labels += (
                empty_core_boundary_fiber_labels
            )
            terminal_tree_productive_empty_core_boundary_fiber_labels += (
                productive_empty_core_boundary_fiber_labels
            )
            terminal_tree_empty_core_boundary_fiber_max_size = max(
                terminal_tree_empty_core_boundary_fiber_max_size,
                empty_core_boundary_fiber_max_size,
            )
            terminal_tree_productive_empty_core_boundary_fiber_max_size = max(
                terminal_tree_productive_empty_core_boundary_fiber_max_size,
                productive_empty_core_boundary_fiber_max_size,
            )
            terminal_tree_empty_core_boundary_root_linear_checks += (
                empty_core_boundary_root_linear_checks
            )
            terminal_tree_productive_empty_core_boundary_root_linear_checks += (
                productive_empty_core_boundary_root_linear_checks
            )
            terminal_tree_empty_core_boundary_root_linear_hits += (
                empty_core_boundary_root_linear_hits
            )
            terminal_tree_productive_empty_core_boundary_root_linear_hits += (
                productive_empty_core_boundary_root_linear_hits
            )
            terminal_tree_empty_core_boundary_complement_pair_checks += (
                empty_core_boundary_complement_pair_checks
            )
            terminal_tree_productive_empty_core_boundary_complement_pair_checks += (
                productive_empty_core_boundary_complement_pair_checks
            )
            terminal_tree_moment_complete_core_checks += (
                moment_complete_core_checks
            )
            terminal_tree_productive_moment_complete_core_checks += (
                productive_moment_complete_core_checks
            )
            terminal_tree_moment_complete_core_max_fiber_size = max(
                terminal_tree_moment_complete_core_max_fiber_size,
                moment_complete_core_max_fiber_size,
            )
            terminal_tree_productive_moment_complete_core_max_fiber_size = max(
                terminal_tree_productive_moment_complete_core_max_fiber_size,
                productive_moment_complete_core_max_fiber_size,
            )
            terminal_tree_deficit_packing_core_checks += (
                deficit_packing_core_checks
            )
            terminal_tree_productive_deficit_packing_core_checks += (
                productive_deficit_packing_core_checks
            )
            terminal_tree_deficit_packing_core_max_deficit = max(
                terminal_tree_deficit_packing_core_max_deficit,
                deficit_packing_core_max_deficit,
            )
            terminal_tree_productive_deficit_packing_core_max_deficit = max(
                terminal_tree_productive_deficit_packing_core_max_deficit,
                productive_deficit_packing_core_max_deficit,
            )
            terminal_tree_deficit_packing_core_max_fiber_size = max(
                terminal_tree_deficit_packing_core_max_fiber_size,
                deficit_packing_core_max_fiber_size,
            )
            terminal_tree_productive_deficit_packing_core_max_fiber_size = max(
                terminal_tree_productive_deficit_packing_core_max_fiber_size,
                productive_deficit_packing_core_max_fiber_size,
            )
            terminal_tree_deficit_anchor_label_checks += (
                deficit_anchor_label_checks
            )
            terminal_tree_productive_deficit_anchor_label_checks += (
                productive_deficit_anchor_label_checks
            )
            terminal_tree_deficit_anchor_max_labels_per_fiber = max(
                terminal_tree_deficit_anchor_max_labels_per_fiber,
                deficit_anchor_max_labels_per_fiber,
            )
            terminal_tree_productive_deficit_anchor_max_labels_per_fiber = max(
                terminal_tree_productive_deficit_anchor_max_labels_per_fiber,
                productive_deficit_anchor_max_labels_per_fiber,
            )
            terminal_tree_deficit_anchor_kernel_checks += (
                deficit_anchor_kernel_checks
            )
            terminal_tree_productive_deficit_anchor_kernel_checks += (
                productive_deficit_anchor_kernel_checks
            )
            terminal_tree_deficit_anchor_max_residual_size = max(
                terminal_tree_deficit_anchor_max_residual_size,
                deficit_anchor_max_residual_size,
            )
            terminal_tree_productive_deficit_anchor_max_residual_size = max(
                terminal_tree_productive_deficit_anchor_max_residual_size,
                productive_deficit_anchor_max_residual_size,
            )
            terminal_tree_deficit_anchor_residual_fiber_checks += (
                deficit_anchor_residual_fiber_checks
            )
            terminal_tree_productive_deficit_anchor_residual_fiber_checks += (
                productive_deficit_anchor_residual_fiber_checks
            )
            terminal_tree_deficit_anchor_residual_fiber_labels += (
                deficit_anchor_residual_fiber_labels
            )
            terminal_tree_productive_deficit_anchor_residual_fiber_labels += (
                productive_deficit_anchor_residual_fiber_labels
            )
            terminal_tree_deficit_anchor_residual_fiber_max_size = max(
                terminal_tree_deficit_anchor_residual_fiber_max_size,
                deficit_anchor_residual_fiber_max_size,
            )
            terminal_tree_productive_deficit_anchor_residual_fiber_max_size = max(
                terminal_tree_productive_deficit_anchor_residual_fiber_max_size,
                productive_deficit_anchor_residual_fiber_max_size,
            )
            terminal_tree_deficit_anchor_residual_fiber_max_direction = max(
                terminal_tree_deficit_anchor_residual_fiber_max_direction,
                deficit_anchor_residual_fiber_max_direction,
            )
            terminal_tree_productive_deficit_anchor_residual_fiber_max_direction = max(
                terminal_tree_productive_deficit_anchor_residual_fiber_max_direction,
                productive_deficit_anchor_residual_fiber_max_direction,
            )
            terminal_tree_deficit_anchor_line_kernel_checks += (
                deficit_anchor_line_kernel_checks
            )
            terminal_tree_productive_deficit_anchor_line_kernel_checks += (
                productive_deficit_anchor_line_kernel_checks
            )
            terminal_tree_deficit_anchor_line_kernel_max_direction_roots = max(
                terminal_tree_deficit_anchor_line_kernel_max_direction_roots,
                deficit_anchor_line_kernel_max_direction_roots,
            )
            terminal_tree_productive_deficit_anchor_line_kernel_max_direction_roots = max(
                terminal_tree_productive_deficit_anchor_line_kernel_max_direction_roots,
                productive_deficit_anchor_line_kernel_max_direction_roots,
            )
            terminal_tree_deficit_anchor_line_kernel_max_sharp_bound = max(
                terminal_tree_deficit_anchor_line_kernel_max_sharp_bound,
                deficit_anchor_line_kernel_max_sharp_bound,
            )
            terminal_tree_productive_deficit_anchor_line_kernel_max_sharp_bound = max(
                terminal_tree_productive_deficit_anchor_line_kernel_max_sharp_bound,
                productive_deficit_anchor_line_kernel_max_sharp_bound,
            )
            terminal_tree_deficit_anchor_direction_mds_checks += (
                deficit_anchor_direction_mds_checks
            )
            terminal_tree_productive_deficit_anchor_direction_mds_checks += (
                productive_deficit_anchor_direction_mds_checks
            )
            terminal_tree_deficit_anchor_direction_mds_bad_subsets += (
                deficit_anchor_direction_mds_bad_subsets
            )
            terminal_tree_productive_deficit_anchor_direction_mds_bad_subsets += (
                productive_deficit_anchor_direction_mds_bad_subsets
            )
            terminal_tree_deficit_anchor_direction_mds_max_bad_subsets = max(
                terminal_tree_deficit_anchor_direction_mds_max_bad_subsets,
                deficit_anchor_direction_mds_max_bad_subsets,
            )
            terminal_tree_productive_deficit_anchor_direction_mds_max_bad_subsets = max(
                terminal_tree_productive_deficit_anchor_direction_mds_max_bad_subsets,
                productive_deficit_anchor_direction_mds_max_bad_subsets,
            )
            terminal_tree_deficit_anchor_direction_mds_max_bound = max(
                terminal_tree_deficit_anchor_direction_mds_max_bound,
                deficit_anchor_direction_mds_max_bound,
            )
            terminal_tree_productive_deficit_anchor_direction_mds_max_bound = max(
                terminal_tree_productive_deficit_anchor_direction_mds_max_bound,
                productive_deficit_anchor_direction_mds_max_bound,
            )
            terminal_tree_deficit_anchor_root_slice_checks += (
                deficit_anchor_root_slice_checks
            )
            terminal_tree_productive_deficit_anchor_root_slice_checks += (
                productive_deficit_anchor_root_slice_checks
            )
            terminal_tree_deficit_anchor_root_slice_labels += (
                deficit_anchor_root_slice_labels
            )
            terminal_tree_productive_deficit_anchor_root_slice_labels += (
                productive_deficit_anchor_root_slice_labels
            )
            terminal_tree_deficit_anchor_root_slice_bad_labels += (
                deficit_anchor_root_slice_bad_labels
            )
            terminal_tree_productive_deficit_anchor_root_slice_bad_labels += (
                productive_deficit_anchor_root_slice_bad_labels
            )
            terminal_tree_deficit_anchor_root_slice_max_bad_per_anchor = max(
                terminal_tree_deficit_anchor_root_slice_max_bad_per_anchor,
                deficit_anchor_root_slice_max_bad_per_anchor,
            )
            terminal_tree_productive_deficit_anchor_root_slice_max_bad_per_anchor = max(
                terminal_tree_productive_deficit_anchor_root_slice_max_bad_per_anchor,
                productive_deficit_anchor_root_slice_max_bad_per_anchor,
            )
            terminal_tree_deficit_anchor_endpoint_rank_checks += (
                deficit_anchor_endpoint_rank_checks
            )
            terminal_tree_productive_deficit_anchor_endpoint_rank_checks += (
                productive_deficit_anchor_endpoint_rank_checks
            )
            terminal_tree_deficit_anchor_endpoint_rank_defects += (
                deficit_anchor_endpoint_rank_defects
            )
            terminal_tree_productive_deficit_anchor_endpoint_rank_defects += (
                productive_deficit_anchor_endpoint_rank_defects
            )
            terminal_tree_deficit_anchor_endpoint_rank_max_defect = max(
                terminal_tree_deficit_anchor_endpoint_rank_max_defect,
                deficit_anchor_endpoint_rank_max_defect,
            )
            terminal_tree_productive_deficit_anchor_endpoint_rank_max_defect = max(
                terminal_tree_productive_deficit_anchor_endpoint_rank_max_defect,
                productive_deficit_anchor_endpoint_rank_max_defect,
            )

            def audit_core_simple_pole_lifts(
                supports: set[tuple[int, ...]],
                productive: bool,
            ) -> tuple[int, int]:
                packet_checks = 0
                lift_checks = 0
                for total_support in sorted(supports):
                    marked_roots = marked_roots_for_split_support(
                        total_support
                    )
                    marked_support = tuple(sorted(marked_roots))
                    if not marked_support:
                        continue
                    marked_set = set(marked_support)
                    unmarked_core = tuple(
                        index
                        for index in total_support
                        if index not in marked_set
                    )
                    marked_count = len(marked_support)
                    amplitudes: dict[int, int] = {}
                    for root_index in marked_support:
                        root = domain[root_index]
                        denominator = 1
                        for other_root_index in marked_support:
                            if other_root_index == root_index:
                                continue
                            denominator = (
                                denominator
                                * (root - domain[other_root_index])
                            ) % p
                        amplitudes[root_index] = (
                            marked_roots[root_index]
                            * pow(denominator, -1, p)
                        ) % p
                    core_vector = hankel_apply(
                        syn,
                        cached_locator(unmarked_core),
                        t + marked_count,
                        p,
                    )
                    expected_core = tuple(
                        sum(
                            amplitudes[root_index]
                            * pow(domain[root_index], row, p)
                            for root_index in marked_support
                        )
                        % p
                        for row in range(t + marked_count)
                    )
                    if core_vector != expected_core:
                        raise AssertionError(
                            {
                                "kind": (
                                    "productive-"
                                    if productive
                                    else ""
                                )
                                + "canonical-core-full-packet-failed",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "total_split_support": list(total_support),
                                "unmarked_core": list(unmarked_core),
                                "marked_support": list(marked_support),
                                "core_vector": list(core_vector),
                                "expected": list(expected_core),
                            }
                        )
                    packet_checks += 1
                    for unmarked_root_index in unmarked_core:
                        lift_core = tuple(
                            index
                            for index in unmarked_core
                            if index != unmarked_root_index
                        )
                        unmarked_root = domain[unmarked_root_index]
                        lift_vector = hankel_apply(
                            syn,
                            cached_locator(lift_core),
                            t + marked_count + 1,
                            p,
                        )
                        expected_lift = tuple(
                            sum(
                                amplitudes[root_index]
                                * pow(
                                    domain[root_index] - unmarked_root,
                                    -1,
                                    p,
                                )
                                * pow(domain[root_index], row, p)
                                for root_index in marked_support
                            )
                            % p
                            for row in range(t + marked_count + 1)
                        )
                        if lift_vector != expected_lift:
                            raise AssertionError(
                                {
                                    "kind": (
                                        "productive-"
                                        if productive
                                        else ""
                                    )
                                    + "canonical-core-simple-pole-"
                                    "lift-failed",
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "fixed_roots": list(fixed_roots),
                                    "total_split_support": list(
                                        total_support
                                    ),
                                    "unmarked_core": list(unmarked_core),
                                    "deleted_unmarked": (
                                        unmarked_root_index
                                    ),
                                    "marked_support": list(marked_support),
                                    "lift_vector": list(lift_vector),
                                    "expected": list(expected_lift),
                                }
                            )
                        lift_checks += 1
                return packet_checks, lift_checks

            (
                core_packet_checks,
                core_simple_pole_lift_checks,
            ) = audit_core_simple_pole_lifts(
                total_split_supports,
                productive=False,
            )
            (
                productive_core_packet_checks,
                productive_core_simple_pole_lift_checks,
            ) = audit_core_simple_pole_lifts(
                productive_total_split_supports,
                productive=True,
            )
            terminal_tree_core_packet_checks += core_packet_checks
            terminal_tree_productive_core_packet_checks += (
                productive_core_packet_checks
            )
            terminal_tree_core_simple_pole_lift_checks += (
                core_simple_pole_lift_checks
            )
            terminal_tree_productive_core_simple_pole_lift_checks += (
                productive_core_simple_pole_lift_checks
            )

            def audit_unmarked_zero_cubes(
                supports: set[tuple[int, ...]],
                productive: bool,
            ) -> tuple[int, int, int]:
                support_checks = 0
                face_checks = 0
                max_unmarked_roots = 0
                for total_support in sorted(supports):
                    marked_roots = marked_roots_for_split_support(
                        total_support
                    )
                    marked_set = set(marked_roots)
                    unmarked_roots = tuple(
                        index
                        for index in total_support
                        if index not in marked_set
                    )
                    support_checks += 1
                    max_unmarked_roots = max(
                        max_unmarked_roots,
                        len(unmarked_roots),
                    )
                    for deleted_count in range(1, len(unmarked_roots) + 1):
                        for deleted_roots in itertools.combinations(
                            unmarked_roots,
                            deleted_count,
                        ):
                            deleted_set = set(deleted_roots)
                            residual_support = tuple(
                                index
                                for index in total_support
                                if index not in deleted_set
                            )
                            residual_vector = hankel_apply(
                                syn,
                                cached_locator(residual_support),
                                t + deleted_count,
                                p,
                            )
                            if any(residual_vector):
                                raise AssertionError(
                                    {
                                        "kind": (
                                            "productive-"
                                            if productive
                                            else ""
                                        )
                                        + "unmarked-zero-cube-face-"
                                        "failed",
                                        "p": p,
                                        "k": k,
                                        "syndrome": list(syn),
                                        "fixed_roots": list(fixed_roots),
                                        "total_split_support": list(
                                            total_support
                                        ),
                                        "deleted_roots": list(deleted_roots),
                                        "residual_support": list(
                                            residual_support
                                        ),
                                        "residual_vector": list(
                                            residual_vector
                                        ),
                                    }
                                )
                            face_checks += 1
                return support_checks, face_checks, max_unmarked_roots

            (
                unmarked_zero_cube_support_checks,
                unmarked_zero_cube_face_checks,
                unmarked_zero_cube_max_unmarked_roots,
            ) = audit_unmarked_zero_cubes(
                total_split_supports,
                productive=False,
            )
            (
                productive_unmarked_zero_cube_support_checks,
                productive_unmarked_zero_cube_face_checks,
                productive_unmarked_zero_cube_max_unmarked_roots,
            ) = audit_unmarked_zero_cubes(
                productive_total_split_supports,
                productive=True,
            )
            terminal_tree_unmarked_zero_cube_support_checks += (
                unmarked_zero_cube_support_checks
            )
            terminal_tree_productive_unmarked_zero_cube_support_checks += (
                productive_unmarked_zero_cube_support_checks
            )
            terminal_tree_unmarked_zero_cube_face_checks += (
                unmarked_zero_cube_face_checks
            )
            terminal_tree_productive_unmarked_zero_cube_face_checks += (
                productive_unmarked_zero_cube_face_checks
            )
            terminal_tree_unmarked_zero_cube_max_unmarked_roots = max(
                terminal_tree_unmarked_zero_cube_max_unmarked_roots,
                unmarked_zero_cube_max_unmarked_roots,
            )
            terminal_tree_productive_unmarked_zero_cube_max_unmarked_roots = max(
                terminal_tree_productive_unmarked_zero_cube_max_unmarked_roots,
                productive_unmarked_zero_cube_max_unmarked_roots,
            )

            def audit_mixed_marked_zero_cubes(
                supports: set[tuple[int, ...]],
                productive: bool,
            ) -> tuple[int, int, int]:
                support_checks = 0
                face_checks = 0
                max_deleted_unmarked = 0
                for total_support in sorted(supports):
                    marked_roots = marked_roots_for_split_support(
                        total_support
                    )
                    marked_root_indices = sorted(marked_roots)
                    unmarked_roots = tuple(
                        index
                        for index in total_support
                        if index not in set(marked_roots)
                    )
                    support_checks += 1
                    for deleted_count in range(1, len(unmarked_roots) + 1):
                        for deleted_unmarked in itertools.combinations(
                            unmarked_roots,
                            deleted_count,
                        ):
                            max_deleted_unmarked = max(
                                max_deleted_unmarked,
                                deleted_count,
                            )
                            for mode_count in range(
                                1,
                                len(marked_root_indices) + 1,
                            ):
                                for candidate_modes in itertools.combinations(
                                    marked_root_indices,
                                    mode_count,
                                ):
                                    candidate_anchor, expected = (
                                        mixed_marked_subset_packet(
                                            total_support,
                                            deleted_unmarked,
                                            candidate_modes,
                                            marked_roots,
                                        )
                                    )
                                    anchor_vector = hankel_apply(
                                        syn,
                                        cached_locator(candidate_anchor),
                                        (
                                            t
                                            + len(deleted_unmarked)
                                            + mode_count
                                        ),
                                        p,
                                    )
                                    if anchor_vector != tuple(expected):
                                        raise AssertionError(
                                            {
                                                "kind": (
                                                    "productive-"
                                                    if productive
                                                    else ""
                                                )
                                                + "mixed-marked-zero-"
                                                "cube-face-failed",
                                                "p": p,
                                                "k": k,
                                                "syndrome": list(syn),
                                                "fixed_roots": list(
                                                    fixed_roots
                                                ),
                                                "total_split_support": list(
                                                    total_support
                                                ),
                                                "deleted_unmarked": list(
                                                    deleted_unmarked
                                                ),
                                                "candidate_modes": list(
                                                    candidate_modes
                                                ),
                                                "candidate_anchor": list(
                                                    candidate_anchor
                                                ),
                                                "anchor_vector": list(
                                                    anchor_vector
                                                ),
                                                "expected": expected,
                                            }
                                        )
                                    if not any(anchor_vector):
                                        raise AssertionError(
                                            {
                                                "kind": (
                                                    "productive-"
                                                    if productive
                                                    else ""
                                                )
                                                + "mixed-marked-zero-"
                                                "cube-face-zero",
                                                "p": p,
                                                "k": k,
                                                "syndrome": list(syn),
                                                "fixed_roots": list(
                                                    fixed_roots
                                                ),
                                                "total_split_support": list(
                                                    total_support
                                                ),
                                                "deleted_unmarked": list(
                                                    deleted_unmarked
                                                ),
                                                "candidate_modes": list(
                                                    candidate_modes
                                                ),
                                                "candidate_anchor": list(
                                                    candidate_anchor
                                                ),
                                            }
                                        )
                                    face_checks += 1
                return support_checks, face_checks, max_deleted_unmarked

            (
                mixed_marked_zero_cube_support_checks,
                mixed_marked_zero_cube_face_checks,
                mixed_marked_zero_cube_max_deleted_unmarked_roots,
            ) = audit_mixed_marked_zero_cubes(
                total_split_supports,
                productive=False,
            )
            (
                productive_mixed_marked_zero_cube_support_checks,
                productive_mixed_marked_zero_cube_face_checks,
                productive_mixed_marked_zero_cube_max_deleted_unmarked_roots,
            ) = audit_mixed_marked_zero_cubes(
                productive_total_split_supports,
                productive=True,
            )
            terminal_tree_mixed_marked_zero_cube_support_checks += (
                mixed_marked_zero_cube_support_checks
            )
            terminal_tree_productive_mixed_marked_zero_cube_support_checks += (
                productive_mixed_marked_zero_cube_support_checks
            )
            terminal_tree_mixed_marked_zero_cube_face_checks += (
                mixed_marked_zero_cube_face_checks
            )
            terminal_tree_productive_mixed_marked_zero_cube_face_checks += (
                productive_mixed_marked_zero_cube_face_checks
            )
            terminal_tree_mixed_marked_zero_cube_max_deleted_unmarked_roots = max(
                terminal_tree_mixed_marked_zero_cube_max_deleted_unmarked_roots,
                mixed_marked_zero_cube_max_deleted_unmarked_roots,
            )
            terminal_tree_productive_mixed_marked_zero_cube_max_deleted_unmarked_roots = max(
                terminal_tree_productive_mixed_marked_zero_cube_max_deleted_unmarked_roots,
                productive_mixed_marked_zero_cube_max_deleted_unmarked_roots,
            )

            def audit_unmarked_shift_marking(
                supports: set[tuple[int, ...]],
                productive: bool,
            ) -> tuple[int, int, int]:
                support_checks = 0
                root_checks = 0
                max_deleted_roots = 0
                for total_support in sorted(supports):
                    marked_roots = marked_roots_for_split_support(
                        total_support
                    )
                    marked_set = set(marked_roots)
                    unmarked_roots = tuple(
                        index
                        for index in total_support
                        if index not in marked_set
                    )
                    for deleted_count in range(1, len(unmarked_roots) + 1):
                        for deleted_unmarked in itertools.combinations(
                            unmarked_roots,
                            deleted_count,
                        ):
                            deleted_set = set(deleted_unmarked)
                            shifted_support = tuple(
                                index
                                for index in total_support
                                if index not in deleted_set
                            )
                            support_checks += 1
                            max_deleted_roots = max(
                                max_deleted_roots,
                                deleted_count,
                            )
                            for root_index in shifted_support:
                                root = domain[root_index]
                                boundary_support = tuple(
                                    index
                                    for index in shifted_support
                                    if index != root_index
                                )
                                boundary_vector = hankel_apply(
                                    syn,
                                    cached_locator(boundary_support),
                                    t + deleted_count + 1,
                                    p,
                                )
                                if root_index in marked_set:
                                    denominator = 1
                                    for deleted_index in deleted_unmarked:
                                        denominator = (
                                            denominator
                                            * (
                                                root
                                                - domain[deleted_index]
                                            )
                                        ) % p
                                    expected_scalar = (
                                        marked_roots[root_index]
                                        * pow(denominator, -1, p)
                                    ) % p
                                else:
                                    expected_scalar = 0
                                expected_boundary = tuple(
                                    expected_scalar * pow(root, row, p) % p
                                    for row in range(t + deleted_count + 1)
                                )
                                if boundary_vector != expected_boundary:
                                    raise AssertionError(
                                        {
                                            "kind": (
                                                "productive-"
                                                if productive
                                                else ""
                                            )
                                            + "unmarked-shift-marking-"
                                            "failed",
                                            "p": p,
                                            "k": k,
                                            "syndrome": list(syn),
                                            "fixed_roots": list(fixed_roots),
                                            "total_split_support": list(
                                                total_support
                                            ),
                                            "deleted_unmarked": list(
                                                deleted_unmarked
                                            ),
                                            "shifted_support": list(
                                                shifted_support
                                            ),
                                            "root": root_index,
                                            "boundary_vector": list(
                                                boundary_vector
                                            ),
                                            "expected_boundary": list(
                                                expected_boundary
                                            ),
                                        }
                                    )
                                root_checks += 1
                return support_checks, root_checks, max_deleted_roots

            (
                unmarked_shift_marking_support_checks,
                unmarked_shift_marking_root_checks,
                unmarked_shift_marking_max_deleted_roots,
            ) = audit_unmarked_shift_marking(
                total_split_supports,
                productive=False,
            )
            (
                productive_unmarked_shift_marking_support_checks,
                productive_unmarked_shift_marking_root_checks,
                productive_unmarked_shift_marking_max_deleted_roots,
            ) = audit_unmarked_shift_marking(
                productive_total_split_supports,
                productive=True,
            )
            terminal_tree_unmarked_shift_marking_support_checks += (
                unmarked_shift_marking_support_checks
            )
            terminal_tree_productive_unmarked_shift_marking_support_checks += (
                productive_unmarked_shift_marking_support_checks
            )
            terminal_tree_unmarked_shift_marking_root_checks += (
                unmarked_shift_marking_root_checks
            )
            terminal_tree_productive_unmarked_shift_marking_root_checks += (
                productive_unmarked_shift_marking_root_checks
            )
            terminal_tree_unmarked_shift_marking_max_deleted_roots = max(
                terminal_tree_unmarked_shift_marking_max_deleted_roots,
                unmarked_shift_marking_max_deleted_roots,
            )
            terminal_tree_productive_unmarked_shift_marking_max_deleted_roots = max(
                terminal_tree_productive_unmarked_shift_marking_max_deleted_roots,
                productive_unmarked_shift_marking_max_deleted_roots,
            )

            def audit_anchor_split_fibers(
                fibers: dict[
                    tuple[int, tuple[int, ...]],
                    list[tuple[int, ...]],
                ],
                productive: bool,
            ) -> tuple[int, int, int]:
                fiber_checks = 0
                fiber_labels = 0
                max_fiber_size = 0
                for (mode_count, anchor_base), supports in fibers.items():
                    unique_supports = sorted(set(supports))
                    fiber_size = len(unique_supports)
                    fiber_checks += 1
                    fiber_labels += fiber_size
                    max_fiber_size = max(max_fiber_size, fiber_size)
                    if mode_count <= t and fiber_size > 1:
                        raise AssertionError(
                            {
                                "kind": (
                                    "productive-"
                                    if productive
                                    else ""
                                )
                                + "anchor-split-fiber-uniqueness-failed",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "anchor_base": list(anchor_base),
                                "mode_count": mode_count,
                                "supports": [
                                    list(support)
                                    for support in unique_supports
                                ],
                            }
                        )
                    if mode_count == t + 1:
                        for left, right in itertools.combinations(
                            unique_supports,
                            2,
                        ):
                            if set(left) & set(right):
                                raise AssertionError(
                                    {
                                        "kind": (
                                            "productive-"
                                            if productive
                                            else ""
                                        )
                                        + "anchor-split-boundary-"
                                        "overlapping-fiber",
                                        "p": p,
                                        "k": k,
                                        "syndrome": list(syn),
                                        "fixed_roots": list(fixed_roots),
                                        "anchor_base": list(anchor_base),
                                        "mode_count": mode_count,
                                        "left_support": list(left),
                                        "right_support": list(right),
                                    }
                                )
                        matching_bound = (
                            n - len(anchor_base)
                        ) // mode_count
                        if fiber_size > matching_bound:
                            raise AssertionError(
                                {
                                    "kind": (
                                        "productive-"
                                        if productive
                                        else ""
                                    )
                                    + "anchor-split-boundary-"
                                    "matching-bound-failed",
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "fixed_roots": list(fixed_roots),
                                    "anchor_base": list(anchor_base),
                                    "mode_count": mode_count,
                                    "fiber_size": fiber_size,
                                    "matching_bound": matching_bound,
                                }
                            )
                return fiber_checks, fiber_labels, max_fiber_size

            (
                anchor_fiber_checks,
                anchor_fiber_labels,
                anchor_fiber_max_size,
            ) = audit_anchor_split_fibers(
                anchor_split_fibers,
                productive=False,
            )
            (
                productive_anchor_fiber_checks,
                productive_anchor_fiber_labels,
                productive_anchor_fiber_max_size,
            ) = audit_anchor_split_fibers(
                productive_anchor_split_fibers,
                productive=True,
            )
            terminal_tree_anchor_fiber_checks += anchor_fiber_checks
            terminal_tree_productive_anchor_fiber_checks += (
                productive_anchor_fiber_checks
            )
            terminal_tree_anchor_fiber_labels += anchor_fiber_labels
            terminal_tree_productive_anchor_fiber_labels += (
                productive_anchor_fiber_labels
            )
            terminal_tree_anchor_fiber_max_size = max(
                terminal_tree_anchor_fiber_max_size,
                anchor_fiber_max_size,
            )
            terminal_tree_productive_anchor_fiber_max_size = max(
                terminal_tree_productive_anchor_fiber_max_size,
                productive_anchor_fiber_max_size,
            )
            visible_packet_repeated_labels = sum(
                1 for count in visible_packet_productions.values() if count > 1
            )
            productive_visible_packet_repeated_labels = sum(
                1
                for count in productive_visible_packet_productions.values()
                if count > 1
            )
            visible_packet_excess = sum(
                count - 1
                for count in visible_packet_productions.values()
                if count > 1
            )
            productive_visible_packet_excess = sum(
                count - 1
                for count in productive_visible_packet_productions.values()
                if count > 1
            )
            visible_packet_max_fiber_size = max(
                visible_packet_productions.values(),
                default=0,
            )
            productive_visible_packet_max_fiber_size = max(
                productive_visible_packet_productions.values(),
                default=0,
            )
            terminal_tree_visible_packet_labels += len(
                visible_packet_productions
            )
            terminal_tree_productive_visible_packet_labels += len(
                productive_visible_packet_productions
            )
            terminal_tree_visible_packet_repeated_labels += (
                visible_packet_repeated_labels
            )
            terminal_tree_productive_visible_packet_repeated_labels += (
                productive_visible_packet_repeated_labels
            )
            terminal_tree_visible_packet_excess_productions += (
                visible_packet_excess
            )
            terminal_tree_productive_visible_packet_excess_productions += (
                productive_visible_packet_excess
            )
            terminal_tree_visible_packet_max_fiber_size = max(
                terminal_tree_visible_packet_max_fiber_size,
                visible_packet_max_fiber_size,
            )
            terminal_tree_productive_visible_packet_max_fiber_size = max(
                terminal_tree_productive_visible_packet_max_fiber_size,
                productive_visible_packet_max_fiber_size,
            )
            terminal_tree_visible_packet_fiber_size_histogram.update(
                visible_packet_productions.values()
            )
            terminal_tree_productive_visible_packet_fiber_size_histogram.update(
                productive_visible_packet_productions.values()
            )
            if any(syn):
                max_nonzero_terminal_tree_visible_packet_fiber_size = max(
                    max_nonzero_terminal_tree_visible_packet_fiber_size,
                    visible_packet_max_fiber_size,
                )
                max_nonzero_terminal_tree_productive_visible_packet_fiber_size = (
                    max(
                        max_nonzero_terminal_tree_productive_visible_packet_fiber_size,
                        productive_visible_packet_max_fiber_size,
                    )
                )
            terminal_tree_recursion_defect_histogram[tree_recursion_defects] += 1
            terminal_tree_branch_vertex_histogram[audit_branch_vertices] += 1
            terminal_tree_branch_pair_histogram[audit_branch_pairs] += 1
            terminal_tree_productive_branch_pair_histogram[
                audit_productive_branch_pairs
            ] += 1
            terminal_tree_mode_packet_histogram[audit_mode_packets] += 1
            terminal_tree_productive_mode_packet_histogram[
                audit_productive_mode_packets
            ] += 1
            terminal_tree_mode_rank_histogram[audit_mode_rank_checks] += 1
            terminal_tree_productive_mode_rank_histogram[
                audit_productive_mode_rank_checks
            ] += 1
            terminal_tree_mode_peeling_histogram[audit_mode_peeling_checks] += 1
            terminal_tree_productive_mode_peeling_histogram[
                audit_productive_mode_peeling_checks
            ] += 1
            terminal_tree_mode_annihilator_histogram[
                audit_mode_annihilator_checks
            ] += 1
            terminal_tree_productive_mode_annihilator_histogram[
                audit_productive_mode_annihilator_checks
            ] += 1
            terminal_tree_multiflag_core_histogram[audit_multiflag_cores] += 1
            if any(syn):
                max_nonzero_terminal_tree_multiflag_cores = max(
                    max_nonzero_terminal_tree_multiflag_cores,
                    audit_multiflag_cores,
                )
            terminal_support_capacity = sum(
                math.factorial(len(core)) for core in terminal_supports
            )
            terminal_support_bound_capacity += terminal_support_capacity
            terminal_bottom_support_checks += len(terminal_supports)
            terminal_support_slack = terminal_support_capacity - audit_terminal_paths
            if terminal_support_slack < 0:
                case_filtration_path_defect += 1
                raise AssertionError(
                    {
                        "kind": "terminal-support-bound-failed",
                        "p": p,
                        "k": k,
                        "syndrome": list(syn),
                        "fixed_roots": list(fixed_roots),
                        "terminal_supports": [
                            list(core) for core in sorted(terminal_supports)
                        ],
                        "terminal_paths": audit_terminal_paths,
                        "capacity": terminal_support_capacity,
                        "slack": terminal_support_slack,
                    }
                )
            terminal_support_bound_slack_histogram[terminal_support_slack] += 1
            if any(syn):
                max_nonzero_terminal_bottom_supports = max(
                    max_nonzero_terminal_bottom_supports,
                    len(terminal_supports),
                )
                max_nonzero_terminal_support_bound_slack = max(
                    max_nonzero_terminal_support_bound_slack,
                    terminal_support_slack,
                )

        active = [
            index
            for index, locator in enumerate(locators)
            if hankel_annihilates(syn, locator, t, p)
        ]
        active_histogram[len(active)] += 1
        max_active = max(max_active, len(active))

        case_edges = 0
        case_edge_cores: set[tuple[int, ...]] = set()
        for left, right in itertools.combinations(active, 2):
            if not is_one_exchange(complements[left], complements[right], j):
                continue
            case_edges += 1
            core = tuple(sorted(set(complements[left]) & set(complements[right])))
            case_edge_cores.add(core)
            core_locator = locator_coeffs(domain, core, p)
            if not hankel_annihilates(syn, core_locator, t + 1, p):
                raise AssertionError(
                    {
                        "kind": "edge-core-lift-failed",
                        "p": p,
                        "k": k,
                        "syndrome": list(syn),
                        "left": list(complements[left]),
                        "right": list(complements[right]),
                        "core": list(core),
                        "core_locator": list(core_locator),
                    }
                )
        one_exchange_edges += case_edges
        edge_histogram[case_edges] += 1
        max_edges = max(max_edges, case_edges)

        case_triangles = 0
        for triangle in itertools.combinations(active, 3):
            triangle_complements = [complements[index] for index in triangle]
            if not all(
                is_one_exchange(left, right, j)
                for left, right in itertools.combinations(triangle_complements, 2)
            ):
                continue
            case_triangles += 1
            kind, packet = classify_triangle(triangle_complements, j)
            if kind == "star":
                star_triangles += 1
                packet_locator = locator_coeffs(domain, packet, p)
                row_count = t + 1
                if len(star_examples) < max_examples:
                    star_examples.append(
                        {
                            "syndrome": list(syn),
                            "complements": [
                                list(complement) for complement in triangle_complements
                            ],
                            "core": list(packet),
                        }
                    )
            else:
                top_triangles += 1
                if any(syn):
                    nonzero_top_triangles += 1
                packet_locator = locator_coeffs(domain, packet, p)
                row_count = 1
                if len(top_examples) < max_examples:
                    top_examples.append(
                        {
                            "syndrome": list(syn),
                            "complements": [
                                list(complement) for complement in triangle_complements
                            ],
                            "top": list(packet),
                            "nonzero_syndrome": bool(any(syn)),
                        }
                    )

            if not hankel_annihilates(syn, packet_locator, row_count, p):
                raise AssertionError(
                    {
                        "kind": f"{kind}-triangle-lift-failed",
                        "p": p,
                        "k": k,
                        "syndrome": list(syn),
                        "complements": [
                            list(complement) for complement in triangle_complements
                        ],
                        "packet": list(packet),
                        "packet_locator": list(packet_locator),
                    }
                )

        triangle_histogram[case_triangles] += 1
        max_triangles = max(max_triangles, case_triangles)

        active_set = set(active)
        audit_filtration_paths(
            (),
            {complements[index] for index in active},
        )
        case_first_boundary_zero_cores: set[tuple[int, ...]] = set()
        case_first_boundary_root_marked: set[tuple[tuple[int, ...], int]] = set()
        for core in itertools.combinations(range(n), j - 1):
            core_set = set(core)
            boundary_vector = hankel_apply(syn, cached_locator(core), t + 1, p)
            if not any(boundary_vector):
                case_first_boundary_zero_cores.add(core)
                for root_index in range(n):
                    if root_index in core_set:
                        continue
                    extension = tuple(sorted((*core, root_index)))
                    if complement_index[extension] not in active_set:
                        raise AssertionError(
                            {
                                "kind": "zero-boundary-core-extension-inactive",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "core": list(core),
                                "extension": list(extension),
                            }
                        )
                continue

            if boundary_vector[0] == 0:
                continue
            root = boundary_vector[1] * pow(boundary_vector[0], -1, p) % p
            if not all(
                boundary_vector[row + 1] == root * boundary_vector[row] % p
                for row in range(t)
            ):
                continue
            root_index = domain_index_by_value.get(root)
            if root_index is None or root_index in core_set:
                continue
            case_first_boundary_root_marked.add((core, root_index))
            extension = tuple(sorted((*core, root_index)))
            if complement_index[extension] not in active_set:
                raise AssertionError(
                    {
                        "kind": "root-marked-boundary-extension-inactive",
                        "p": p,
                        "k": k,
                        "syndrome": list(syn),
                        "core": list(core),
                        "root_index": root_index,
                        "root_value": root,
                        "boundary_vector": list(boundary_vector),
                        "extension": list(extension),
                    }
                )

        if case_first_boundary_zero_cores != case_edge_cores:
            raise AssertionError(
                {
                    "kind": "edge-core-zero-boundary-mismatch",
                    "p": p,
                    "k": k,
                    "syndrome": list(syn),
                    "zero_boundary_only": [
                        list(core)
                        for core in sorted(
                            case_first_boundary_zero_cores - case_edge_cores
                        )
                    ],
                    "edge_core_only": [
                        list(core)
                        for core in sorted(
                            case_edge_cores - case_first_boundary_zero_cores
                        )
                    ],
                }
            )

        case_isolated_vertices = 0
        case_root_marked_boundaries: set[tuple[tuple[int, ...], int]] = set()
        for index in active:
            complement = complements[index]
            has_active_neighbor = any(
                neighbor in active_set for neighbor in one_exchange_neighbors[index]
            )
            zero_boundary_count = 0
            for root_index in complement:
                root = domain[root_index]
                core = tuple(item for item in complement if item != root_index)
                boundary_vector = hankel_apply(syn, cached_locator(core), t + 1, p)
                for row in range(t):
                    if boundary_vector[row + 1] != root * boundary_vector[row] % p:
                        raise AssertionError(
                            {
                                "kind": "isolated-boundary-veronese-failed",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "complement": list(complement),
                                "deleted_root": root_index,
                                "root_value": root,
                                "boundary_vector": list(boundary_vector),
                            }
                        )
                boundary_is_zero = not any(boundary_vector)
                if (boundary_vector[0] == 0) != boundary_is_zero:
                    raise AssertionError(
                        {
                            "kind": "isolated-boundary-zero-scalar-mismatch",
                            "p": p,
                            "k": k,
                            "syndrome": list(syn),
                            "complement": list(complement),
                            "deleted_root": root_index,
                            "boundary_vector": list(boundary_vector),
                        }
                    )
                if boundary_is_zero:
                    zero_boundary_count += 1
                else:
                    case_root_marked_boundaries.add((core, root_index))

            is_isolated = not has_active_neighbor
            if is_isolated != (zero_boundary_count == 0):
                raise AssertionError(
                    {
                        "kind": "isolated-vertex-criterion-failed",
                        "p": p,
                        "k": k,
                        "syndrome": list(syn),
                        "complement": list(complement),
                        "has_active_neighbor": has_active_neighbor,
                        "zero_boundary_count": zero_boundary_count,
                    }
                )
            if is_isolated:
                case_isolated_vertices += 1
            isolated_boundary_zero_histogram[zero_boundary_count] += 1

        if case_root_marked_boundaries != case_first_boundary_root_marked:
            raise AssertionError(
                {
                    "kind": "active-root-marked-boundary-mismatch",
                    "p": p,
                    "k": k,
                    "syndrome": list(syn),
                    "active_only": [
                        (list(core), root)
                        for core, root in sorted(
                            case_root_marked_boundaries
                            - case_first_boundary_root_marked
                        )
                    ],
                    "boundary_only": [
                        (list(core), root)
                        for core, root in sorted(
                            case_first_boundary_root_marked
                            - case_root_marked_boundaries
                        )
                    ],
                }
            )
        first_boundary_incidence_defect = j * len(active) - (
            (n - j + 1) * len(case_first_boundary_zero_cores)
            + len(case_root_marked_boundaries)
        )
        if first_boundary_incidence_defect != 0:
            raise AssertionError(
                {
                    "kind": "first-boundary-incidence-identity-failed",
                    "p": p,
                    "k": k,
                    "syndrome": list(syn),
                    "active_complements": len(active),
                    "zero_boundary_cores": len(case_first_boundary_zero_cores),
                    "root_marked_boundaries": len(case_root_marked_boundaries),
                    "defect": first_boundary_incidence_defect,
                    "j": j,
                }
            )
        first_boundary_zero_core_histogram[len(case_first_boundary_zero_cores)] += 1
        first_boundary_incidence_defect_histogram[
            first_boundary_incidence_defect
        ] += 1
        fixed_root_active_counts: Counter[int] = Counter()
        for index in active:
            fixed_root_active_counts.update(complements[index])
        fixed_root_zero_core_counts: Counter[int] = Counter()
        for core in case_first_boundary_zero_cores:
            core_set = set(core)
            for root_index in range(n):
                if root_index not in core_set:
                    fixed_root_zero_core_counts[root_index] += 1
        root_marked_counts: Counter[int] = Counter(
            root_index for _, root_index in case_root_marked_boundaries
        )
        case_max_fixed_root_defect = 0
        for root_index in range(n):
            fixed_root_defect = (
                fixed_root_active_counts[root_index]
                - fixed_root_zero_core_counts[root_index]
                - root_marked_counts[root_index]
            )
            case_max_fixed_root_defect = max(
                case_max_fixed_root_defect,
                abs(fixed_root_defect),
            )
            if fixed_root_defect != 0:
                raise AssertionError(
                    {
                        "kind": "fixed-root-boundary-decomposition-failed",
                        "p": p,
                        "k": k,
                        "syndrome": list(syn),
                        "root_index": root_index,
                        "root_value": domain[root_index],
                        "fixed_root_active": fixed_root_active_counts[root_index],
                        "zero_boundary_available": fixed_root_zero_core_counts[
                            root_index
                        ],
                        "root_marked": root_marked_counts[root_index],
                        "defect": fixed_root_defect,
                    }
                )
        fixed_root_decomposition_defect_histogram[case_max_fixed_root_defect] += 1
        case_max_fixed_root_difference_defect = 0
        case_max_fixed_root_difference_kernel_count = 0
        for root_index, root in enumerate(domain):
            diff_syn = root_difference_syndrome(syn, root, p)
            difference_kernel_cores: set[tuple[int, ...]] = set()
            for core in itertools.combinations(
                (index for index in range(n) if index != root_index),
                j - 1,
            ):
                if hankel_annihilates(diff_syn, cached_locator(core), t, p):
                    difference_kernel_cores.add(core)
                    extension = tuple(sorted((*core, root_index)))
                    if complement_index[extension] not in active_set:
                        raise AssertionError(
                            {
                                "kind": "root-difference-kernel-extension-inactive",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "root_index": root_index,
                                "root_value": root,
                                "core": list(core),
                                "extension": list(extension),
                            }
                        )
            fixed_root_active_cores = {
                tuple(
                    index
                    for index in complements[active_index]
                    if index != root_index
                )
                for active_index in active
                if root_index in complements[active_index]
            }
            if difference_kernel_cores != fixed_root_active_cores:
                raise AssertionError(
                    {
                        "kind": "fixed-root-difference-kernel-mismatch",
                        "p": p,
                        "k": k,
                        "syndrome": list(syn),
                        "root_index": root_index,
                        "root_value": root,
                        "difference_only": [
                            list(core)
                            for core in sorted(
                                difference_kernel_cores - fixed_root_active_cores
                            )
                        ],
                        "active_only": [
                            list(core)
                            for core in sorted(
                                fixed_root_active_cores - difference_kernel_cores
                            )
                        ],
                    }
                )
            difference_residual = (
                difference_kernel_cores - case_first_boundary_zero_cores
            )
            root_marked_cores = {
                core
                for core, marked_root_index in case_root_marked_boundaries
                if marked_root_index == root_index
            }
            if difference_residual != root_marked_cores:
                raise AssertionError(
                    {
                        "kind": "root-difference-residual-mismatch",
                        "p": p,
                        "k": k,
                        "syndrome": list(syn),
                        "root_index": root_index,
                        "root_value": root,
                        "residual_only": [
                            list(core)
                            for core in sorted(difference_residual - root_marked_cores)
                        ],
                        "marked_only": [
                            list(core)
                            for core in sorted(root_marked_cores - difference_residual)
                        ],
                    }
                )
            case_max_fixed_root_difference_defect = max(
                case_max_fixed_root_difference_defect,
                abs(
                    len(difference_kernel_cores)
                    - fixed_root_active_counts[root_index]
                ),
            )
            case_max_fixed_root_difference_kernel_count = max(
                case_max_fixed_root_difference_kernel_count,
                len(difference_kernel_cores),
            )
        fixed_root_difference_defect_histogram[
            case_max_fixed_root_difference_defect
        ] += 1
        case_max_root_marked_single_row_defect = 0
        case_max_root_marked_single_row_count = 0
        case_root_marked_slice_edges = 0
        case_root_marked_edge_cores: set[tuple[int, tuple[int, ...]]] = set()
        case_root_marked_nonisolated: set[tuple[int, tuple[int, ...]]] = set()
        case_root_marked_isolated_count = 0
        case_residual_boundaries: set[tuple[int, tuple[int, ...], int]] = set()
        for root_index in range(n):
            diff_syn = root_difference_syndrome(syn, domain[root_index], p)
            difference_kernel_cores = {
                core
                for core in itertools.combinations(
                    (index for index in range(n) if index != root_index),
                    j - 1,
                )
                if hankel_annihilates(diff_syn, cached_locator(core), t, p)
            }
            single_row_zero_cores = {
                core
                for core in difference_kernel_cores
                if not hankel_apply(syn, cached_locator(core), 1, p)[0]
            }
            zero_boundary_cores = {
                core
                for core in case_first_boundary_zero_cores
                if root_index not in core
            }
            if single_row_zero_cores != zero_boundary_cores:
                raise AssertionError(
                    {
                        "kind": "single-row-zero-boundary-mismatch",
                        "p": p,
                        "k": k,
                        "syndrome": list(syn),
                        "root_index": root_index,
                        "root_value": domain[root_index],
                        "single_row_only": [
                            list(core)
                            for core in sorted(
                                single_row_zero_cores - zero_boundary_cores
                            )
                        ],
                        "zero_boundary_only": [
                            list(core)
                            for core in sorted(
                                zero_boundary_cores - single_row_zero_cores
                            )
                        ],
                    }
                )
            single_row_nonzero_cores = (
                difference_kernel_cores - single_row_zero_cores
            )
            root_marked_cores = {
                core
                for core, marked_root_index in case_root_marked_boundaries
                if marked_root_index == root_index
            }
            if single_row_nonzero_cores != root_marked_cores:
                raise AssertionError(
                    {
                        "kind": "root-marked-single-row-slice-mismatch",
                        "p": p,
                        "k": k,
                        "syndrome": list(syn),
                        "root_index": root_index,
                        "root_value": domain[root_index],
                        "single_row_only": [
                            list(core)
                            for core in sorted(
                                single_row_nonzero_cores - root_marked_cores
                            )
                        ],
                        "marked_only": [
                            list(core)
                            for core in sorted(
                                root_marked_cores - single_row_nonzero_cores
                            )
                        ],
                    }
                )
            case_max_root_marked_single_row_defect = max(
                case_max_root_marked_single_row_defect,
                abs(len(single_row_nonzero_cores) - root_marked_counts[root_index]),
            )
            case_max_root_marked_single_row_count = max(
                case_max_root_marked_single_row_count,
                len(single_row_nonzero_cores),
            )
            local_root_marked_nonisolated: set[tuple[int, ...]] = set()
            if j >= 2:
                for left, right in itertools.combinations(
                    sorted(single_row_nonzero_cores),
                    2,
                ):
                    common = tuple(sorted(set(left) & set(right)))
                    if len(common) != j - 2:
                        continue
                    case_root_marked_slice_edges += 1
                    local_root_marked_nonisolated.add(left)
                    local_root_marked_nonisolated.add(right)
                    case_root_marked_nonisolated.add((root_index, left))
                    case_root_marked_nonisolated.add((root_index, right))
                    case_root_marked_edge_cores.add((root_index, common))
                    if not hankel_annihilates(
                        diff_syn,
                        cached_locator(common),
                        t + 1,
                        p,
                    ):
                        raise AssertionError(
                            {
                                "kind": "root-marked-edge-descent-failed",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "root_index": root_index,
                                "root_value": domain[root_index],
                                "left": list(left),
                                "right": list(right),
                                "lower_core": list(common),
                            }
                        )
            local_root_marked_isolated = (
                single_row_nonzero_cores - local_root_marked_nonisolated
            )
            case_root_marked_isolated_count += len(local_root_marked_isolated)
            for core in single_row_nonzero_cores:
                zero_lower_boundary_count = 0
                for deleted_root_index in core:
                    lower_core = tuple(
                        entry for entry in core if entry != deleted_root_index
                    )
                    lower_boundary = hankel_apply(
                        diff_syn,
                        cached_locator(lower_core),
                        t + 1,
                        p,
                    )
                    deleted_root = domain[deleted_root_index]
                    for row in range(t):
                        if (
                            lower_boundary[row + 1]
                            != deleted_root * lower_boundary[row] % p
                        ):
                            raise AssertionError(
                                {
                                    "kind": (
                                        "root-marked-lower-boundary-"
                                        "veronese-failed"
                                    ),
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "root_index": root_index,
                                    "fixed_root": domain[root_index],
                                    "core": list(core),
                                    "deleted_root": deleted_root_index,
                                    "deleted_root_value": deleted_root,
                                    "lower_boundary": list(lower_boundary),
                                }
                            )
                    if not any(lower_boundary):
                        zero_lower_boundary_count += 1
                    else:
                        case_residual_boundaries.add(
                            (root_index, lower_core, deleted_root_index)
                        )
                criterion_isolated = zero_lower_boundary_count == 0
                if (n - j >= 2 or j <= 1) and (
                    (core in local_root_marked_isolated) != criterion_isolated
                ):
                    raise AssertionError(
                        {
                            "kind": "root-marked-isolated-criterion-failed",
                            "p": p,
                            "k": k,
                            "syndrome": list(syn),
                            "root_index": root_index,
                            "root_value": domain[root_index],
                            "core": list(core),
                            "actual_isolated": core
                            in local_root_marked_isolated,
                            "zero_lower_boundary_count": (
                                zero_lower_boundary_count
                            ),
                            "j": j,
                            "n": n,
                        }
                    )
        root_marked_single_row_defect_histogram[
            case_max_root_marked_single_row_defect
        ] += 1
        root_marked_edge_capacity = (n - j + 1) * len(case_root_marked_edge_cores)
        root_marked_edge_slack = (
            root_marked_edge_capacity - len(case_root_marked_nonisolated)
        )
        if root_marked_edge_slack < 0:
            raise AssertionError(
                {
                    "kind": "root-marked-edge-core-ledger-failed",
                    "p": p,
                    "k": k,
                    "syndrome": list(syn),
                    "root_marked_nonisolated": len(case_root_marked_nonisolated),
                    "root_marked_edge_core_count": len(case_root_marked_edge_cores),
                    "root_marked_edge_capacity": root_marked_edge_capacity,
                }
            )
        root_marked_edge_core_slack_histogram[root_marked_edge_slack] += 1
        residual_boundary_slack = len(case_residual_boundaries) - (
            (j - 1) * case_root_marked_isolated_count
        )
        if residual_boundary_slack < 0:
            raise AssertionError(
                {
                    "kind": "root-marked-isolated-boundary-ledger-failed",
                    "p": p,
                    "k": k,
                    "syndrome": list(syn),
                    "root_marked_isolated": case_root_marked_isolated_count,
                    "residual_boundaries": len(case_residual_boundaries),
                    "j": j,
                }
            )
        root_marked_isolated_histogram[case_root_marked_isolated_count] += 1
        residual_boundary_slack_histogram[residual_boundary_slack] += 1
        case_iterated_difference_defect = 0
        for chain_length in range(1, j + 1):
            row_count = t
            if row_count > len(syn) - chain_length:
                continue
            max_iterated_difference_chain_length = max(
                max_iterated_difference_chain_length,
                chain_length,
            )
            for fixed_roots in itertools.combinations(range(n), chain_length):
                fixed_values = [domain[index] for index in fixed_roots]
                diff_syn = iterated_root_difference_syndrome(
                    syn,
                    fixed_values,
                    p,
                )
                remaining_indices = [
                    index for index in range(n) if index not in fixed_roots
                ]
                for core in itertools.combinations(
                    remaining_indices,
                    j - chain_length,
                ):
                    full_locator = cached_locator(tuple(sorted((*core, *fixed_roots))))
                    core_locator = cached_locator(core)
                    direct = hankel_apply(syn, full_locator, row_count, p)
                    differenced = hankel_apply(
                        diff_syn,
                        core_locator,
                        row_count,
                        p,
                    )
                    iterated_difference_checks += 1
                    if direct != differenced:
                        case_iterated_difference_defect += 1
                        raise AssertionError(
                            {
                                "kind": "iterated-root-difference-identity-failed",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "fixed_values": fixed_values,
                                "core": list(core),
                                "direct": list(direct),
                                "differenced": list(differenced),
                            }
                        )
        iterated_difference_defect_histogram[case_iterated_difference_defect] += 1
        case_iterated_boundary_defect = 0
        case_fixed_root_filtration_defect = 0
        case_max_iterated_boundary_active_cores = 0
        case_max_iterated_boundary_zero_cores = 0
        case_max_iterated_boundary_marked = 0
        case_max_fixed_root_filtration_pairs = 0
        for chain_length in range(1, j):
            quotient_degree = j - chain_length
            max_iterated_boundary_chain_length = max(
                max_iterated_boundary_chain_length,
                chain_length,
            )
            for fixed_roots in itertools.combinations(range(n), chain_length):
                fixed_values = [domain[index] for index in fixed_roots]
                fixed_root_set = set(fixed_roots)
                diff_syn = iterated_root_difference_syndrome(
                    syn,
                    fixed_values,
                    p,
                )
                remaining_indices = [
                    index for index in range(n) if index not in fixed_root_set
                ]
                active_cores = {
                    core
                    for core in itertools.combinations(
                        remaining_indices,
                        quotient_degree,
                    )
                    if hankel_annihilates(diff_syn, cached_locator(core), t, p)
                }
                audit_filtration_paths(fixed_roots, active_cores)
                zero_boundary_cores: set[tuple[int, ...]] = set()
                root_marked_boundaries: set[tuple[tuple[int, ...], int]] = set()
                for boundary_core in itertools.combinations(
                    remaining_indices,
                    quotient_degree - 1,
                ):
                    boundary_core_set = set(boundary_core)
                    boundary_vector = hankel_apply(
                        diff_syn,
                        cached_locator(boundary_core),
                        t + 1,
                        p,
                    )
                    available_extensions = [
                        index
                        for index in remaining_indices
                        if index not in boundary_core_set
                    ]
                    if not any(boundary_vector):
                        zero_boundary_cores.add(boundary_core)
                        for extension_root in available_extensions:
                            extension = tuple(
                                sorted((*boundary_core, extension_root))
                            )
                            if extension not in active_cores:
                                raise AssertionError(
                                    {
                                        "kind": (
                                            "iterated-zero-boundary-"
                                            "extension-inactive"
                                        ),
                                        "p": p,
                                        "k": k,
                                        "syndrome": list(syn),
                                        "fixed_roots": list(fixed_roots),
                                        "fixed_values": fixed_values,
                                        "boundary_core": list(boundary_core),
                                        "extension": list(extension),
                                    }
                                )
                        continue
                    if boundary_vector[0] == 0:
                        continue
                    root_value = (
                        boundary_vector[1] * pow(boundary_vector[0], -1, p)
                    ) % p
                    if any(
                        boundary_vector[row + 1]
                        != root_value * boundary_vector[row] % p
                        for row in range(t)
                    ):
                        continue
                    root_index = domain_index_by_value.get(root_value)
                    if (
                        root_index is None
                        or root_index in fixed_root_set
                        or root_index in boundary_core_set
                    ):
                        continue
                    extension = tuple(sorted((*boundary_core, root_index)))
                    if extension not in active_cores:
                        raise AssertionError(
                            {
                                "kind": (
                                    "iterated-root-marked-boundary-"
                                    "extension-inactive"
                                ),
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "fixed_roots": list(fixed_roots),
                                "fixed_values": fixed_values,
                                "boundary_core": list(boundary_core),
                                "root_index": root_index,
                                "root_value": root_value,
                                "boundary_vector": list(boundary_vector),
                            }
                        )
                    root_marked_boundaries.add((boundary_core, root_index))
                incidence_defect = quotient_degree * len(active_cores) - (
                    (n - j + 1) * len(zero_boundary_cores)
                    + len(root_marked_boundaries)
                )
                active_incidence_pairs = {
                    (
                        tuple(entry for entry in core if entry != root_index),
                        root_index,
                    )
                    for core in active_cores
                    for root_index in core
                }
                boundary_partition_pairs = set(root_marked_boundaries)
                for boundary_core in zero_boundary_cores:
                    boundary_core_set = set(boundary_core)
                    for root_index in remaining_indices:
                        if root_index not in boundary_core_set:
                            boundary_partition_pairs.add(
                                (boundary_core, root_index)
                            )
                fixed_root_filtration_pair_checks += len(active_incidence_pairs)
                if active_incidence_pairs != boundary_partition_pairs:
                    case_fixed_root_filtration_defect += 1
                    raise AssertionError(
                        {
                            "kind": "fixed-root-filtration-identity-failed",
                            "p": p,
                            "k": k,
                            "syndrome": list(syn),
                            "fixed_roots": list(fixed_roots),
                            "fixed_values": fixed_values,
                            "quotient_degree": quotient_degree,
                            "active_only": [
                                [list(core), root]
                                for core, root in sorted(
                                    active_incidence_pairs
                                    - boundary_partition_pairs
                                )
                            ],
                            "boundary_only": [
                                [list(core), root]
                                for core, root in sorted(
                                    boundary_partition_pairs
                                    - active_incidence_pairs
                                )
                            ],
                        }
                    )
                iterated_boundary_identity_checks += 1
                if incidence_defect != 0:
                    case_iterated_boundary_defect += abs(incidence_defect)
                    raise AssertionError(
                        {
                            "kind": "iterated-boundary-identity-failed",
                            "p": p,
                            "k": k,
                            "syndrome": list(syn),
                            "fixed_roots": list(fixed_roots),
                            "fixed_values": fixed_values,
                            "quotient_degree": quotient_degree,
                            "active_cores": len(active_cores),
                            "zero_boundary_cores": len(zero_boundary_cores),
                            "root_marked_boundaries": (
                                len(root_marked_boundaries)
                            ),
                            "defect": incidence_defect,
                        }
                    )
                case_max_iterated_boundary_active_cores = max(
                    case_max_iterated_boundary_active_cores,
                    len(active_cores),
                )
                case_max_iterated_boundary_zero_cores = max(
                    case_max_iterated_boundary_zero_cores,
                    len(zero_boundary_cores),
                )
                case_max_iterated_boundary_marked = max(
                    case_max_iterated_boundary_marked,
                    len(root_marked_boundaries),
                )
                case_max_fixed_root_filtration_pairs = max(
                    case_max_fixed_root_filtration_pairs,
                    len(active_incidence_pairs),
                )
        iterated_boundary_defect_histogram[case_iterated_boundary_defect] += 1
        fixed_root_filtration_defect_histogram[
            case_fixed_root_filtration_defect
        ] += 1
        filtration_path_defect_histogram[case_filtration_path_defect] += 1
        path_partition_defect = case_filtration_paths - (
            case_zero_stop_filtration_paths + case_terminal_filtration_paths
        )
        if path_partition_defect != 0:
            raise AssertionError(
                {
                    "kind": "filtration-path-partition-failed",
                    "p": p,
                    "k": k,
                    "syndrome": list(syn),
                    "paths": case_filtration_paths,
                    "zero_stop_paths": case_zero_stop_filtration_paths,
                    "terminal_paths": case_terminal_filtration_paths,
                    "defect": path_partition_defect,
                }
            )
        filtration_path_partition_defect_histogram[path_partition_defect] += 1
        isolated_marked_boundary_slack = (
            len(case_root_marked_boundaries) - j * case_isolated_vertices
        )
        if isolated_marked_boundary_slack < 0:
            raise AssertionError(
                {
                    "kind": "isolated-marked-boundary-ledger-failed",
                    "p": p,
                    "k": k,
                    "syndrome": list(syn),
                    "isolated_vertices": case_isolated_vertices,
                    "root_marked_boundaries": len(case_root_marked_boundaries),
                    "j": j,
                }
            )
        isolated_marked_boundary_slack_histogram[isolated_marked_boundary_slack] += 1
        isolated_vertex_histogram[case_isolated_vertices] += 1
        if any(syn):
            max_nonzero_isolated_vertices = max(
                max_nonzero_isolated_vertices,
                case_isolated_vertices,
            )
            max_nonzero_root_marked_boundary_count = max(
                max_nonzero_root_marked_boundary_count,
                len(case_root_marked_boundaries),
            )
            max_nonzero_first_boundary_zero_core_count = max(
                max_nonzero_first_boundary_zero_core_count,
                len(case_first_boundary_zero_cores),
            )
            max_nonzero_fixed_root_active_count = max(
                max_nonzero_fixed_root_active_count,
                max(fixed_root_active_counts.values(), default=0),
            )
            max_nonzero_fixed_root_difference_kernel_count = max(
                max_nonzero_fixed_root_difference_kernel_count,
                case_max_fixed_root_difference_kernel_count,
            )
            max_nonzero_root_marked_per_root = max(
                max_nonzero_root_marked_per_root,
                max(root_marked_counts.values(), default=0),
            )
            max_nonzero_root_marked_single_row_count = max(
                max_nonzero_root_marked_single_row_count,
                case_max_root_marked_single_row_count,
            )
            max_nonzero_root_marked_slice_edges = max(
                max_nonzero_root_marked_slice_edges,
                case_root_marked_slice_edges,
            )
            max_nonzero_root_marked_edge_core_count = max(
                max_nonzero_root_marked_edge_core_count,
                len(case_root_marked_edge_cores),
            )
            max_nonzero_root_marked_edge_core_slack = max(
                max_nonzero_root_marked_edge_core_slack,
                root_marked_edge_slack,
            )
            max_nonzero_root_marked_isolated_count = max(
                max_nonzero_root_marked_isolated_count,
                case_root_marked_isolated_count,
            )
            max_nonzero_residual_boundary_count = max(
                max_nonzero_residual_boundary_count,
                len(case_residual_boundaries),
            )
            max_nonzero_residual_boundary_slack = max(
                max_nonzero_residual_boundary_slack,
                residual_boundary_slack,
            )
            max_nonzero_iterated_boundary_active_cores = max(
                max_nonzero_iterated_boundary_active_cores,
                case_max_iterated_boundary_active_cores,
            )
            max_nonzero_iterated_boundary_zero_cores = max(
                max_nonzero_iterated_boundary_zero_cores,
                case_max_iterated_boundary_zero_cores,
            )
            max_nonzero_iterated_boundary_marked = max(
                max_nonzero_iterated_boundary_marked,
                case_max_iterated_boundary_marked,
            )
            max_nonzero_fixed_root_filtration_pairs = max(
                max_nonzero_fixed_root_filtration_pairs,
                case_max_fixed_root_filtration_pairs,
            )
            max_nonzero_filtration_paths = max(
                max_nonzero_filtration_paths,
                case_filtration_paths,
            )
            max_nonzero_zero_stop_filtration_paths = max(
                max_nonzero_zero_stop_filtration_paths,
                case_zero_stop_filtration_paths,
            )
            max_nonzero_terminal_filtration_paths = max(
                max_nonzero_terminal_filtration_paths,
                case_terminal_filtration_paths,
            )
            max_nonzero_filtration_nonzero_scalar_steps = max(
                max_nonzero_filtration_nonzero_scalar_steps,
                case_filtration_nonzero_scalar_steps,
            )
            max_nonzero_isolated_marked_boundary_slack = max(
                max_nonzero_isolated_marked_boundary_slack,
                isolated_marked_boundary_slack,
            )

        case_corner_histogram: Counter[str] = Counter()
        case_lower_core_witnesses: set[tuple[int, ...]] = set()
        for center in active:
            center_set = set(complements[center])
            active_neighbors = [
                neighbor
                for neighbor in one_exchange_neighbors[center]
                if neighbor in active_set
            ]
            for left, right in itertools.combinations(active_neighbors, 2):
                left_deleted = tuple(sorted(center_set - set(complements[left])))
                right_deleted = tuple(sorted(center_set - set(complements[right])))
                if len(left_deleted) != 1 or len(right_deleted) != 1:
                    raise AssertionError(
                        {
                            "kind": "unexpected-corner-deleted-size",
                            "p": p,
                            "k": k,
                            "syndrome": list(syn),
                            "center": list(complements[center]),
                            "left": list(complements[left]),
                            "right": list(complements[right]),
                            "left_deleted": list(left_deleted),
                            "right_deleted": list(right_deleted),
                        }
                    )
                if left_deleted == right_deleted:
                    case_corner_histogram["star"] += 1
                    core = tuple(sorted(center_set - set(left_deleted)))
                    if not hankel_annihilates(syn, cached_locator(core), t + 1, p):
                        raise AssertionError(
                            {
                                "kind": "star-corner-core-lift-failed",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "center": list(complements[center]),
                                "left": list(complements[left]),
                                "right": list(complements[right]),
                                "core": list(core),
                            }
                        )
                    continue

                case_corner_histogram["lower_core"] += 1
                core = tuple(
                    sorted(center_set - set(left_deleted) - set(right_deleted))
                )
                case_lower_core_witnesses.add(core)
                if not hankel_annihilates(syn, cached_locator(core), t + 2, p):
                    raise AssertionError(
                        {
                            "kind": "lower-core-corner-lift-failed",
                            "p": p,
                            "k": k,
                            "syndrome": list(syn),
                            "center": list(complements[center]),
                            "left": list(complements[left]),
                            "right": list(complements[right]),
                            "core": list(core),
                        }
                    )

        corner_histogram.update(case_corner_histogram)
        if any(syn):
            nonzero_corner_histogram.update(case_corner_histogram)
            max_nonzero_star_corners_per_syndrome = max(
                max_nonzero_star_corners_per_syndrome,
                case_corner_histogram["star"],
            )
            max_nonzero_lower_core_corners_per_syndrome = max(
                max_nonzero_lower_core_corners_per_syndrome,
                case_corner_histogram["lower_core"],
            )

        seen_components: set[int] = set()
        case_component_histogram: Counter[str] = Counter()
        case_nonisolated_vertices: set[int] = set()
        for start in active:
            if start in seen_components:
                continue
            stack = [start]
            seen_components.add(start)
            component: list[int] = []
            while stack:
                current = stack.pop()
                component.append(current)
                for neighbor in one_exchange_neighbors[current]:
                    if neighbor not in active_set or neighbor in seen_components:
                        continue
                    seen_components.add(neighbor)
                    stack.append(neighbor)

            if len(component) <= 1:
                continue
            case_nonisolated_vertices.update(component)

            common = set(complements[component[0]])
            for index in component[1:]:
                common &= set(complements[index])

            if len(common) == j - 1:
                core = tuple(sorted(common))
                if not hankel_annihilates(syn, cached_locator(core), t + 1, p):
                    raise AssertionError(
                        {
                            "kind": "star-component-core-lift-failed",
                            "p": p,
                            "k": k,
                            "syndrome": list(syn),
                            "component": [list(complements[index]) for index in component],
                            "core": list(core),
                        }
                    )
                component_kind = "star"
            else:
                lower_core: tuple[int, ...] | None = None
                for center in component:
                    center_set = set(complements[center])
                    active_component_neighbors = [
                        neighbor
                        for neighbor in one_exchange_neighbors[center]
                        if neighbor in component
                    ]
                    for left, right in itertools.combinations(
                        active_component_neighbors,
                        2,
                    ):
                        left_deleted = tuple(
                            sorted(center_set - set(complements[left]))
                        )
                        right_deleted = tuple(
                            sorted(center_set - set(complements[right]))
                        )
                        if left_deleted == right_deleted:
                            continue
                        candidate = tuple(
                            sorted(
                                center_set
                                - set(left_deleted)
                                - set(right_deleted)
                            )
                        )
                        if hankel_annihilates(
                            syn,
                            cached_locator(candidate),
                            t + 2,
                            p,
                        ):
                            lower_core = candidate
                            break
                    if lower_core is not None:
                        break
                if lower_core is None:
                    raise AssertionError(
                        {
                            "kind": "nonstar-component-without-lower-core",
                            "p": p,
                            "k": k,
                            "syndrome": list(syn),
                            "component": [list(complements[index]) for index in component],
                            "common_intersection": sorted(common),
                        }
                    )
                component_kind = "lower_core"

            case_component_histogram[component_kind] += 1
            component_histogram[component_kind] += 1
            component_size_histogram[f"{component_kind}:{len(component)}"] += 1
            if any(syn):
                nonzero_component_histogram[component_kind] += 1
                nonzero_component_size_histogram[
                    f"{component_kind}:{len(component)}"
                ] += 1
                if component_kind == "star":
                    max_nonzero_star_component_size = max(
                        max_nonzero_star_component_size,
                        len(component),
                    )
                else:
                    max_nonzero_lower_core_component_size = max(
                        max_nonzero_lower_core_component_size,
                        len(component),
                    )

        edge_core_capacity = (n - j + 1) * len(case_edge_cores)
        nonisolated_ledger_slack = edge_core_capacity - len(case_nonisolated_vertices)
        if nonisolated_ledger_slack < 0:
            raise AssertionError(
                {
                    "kind": "nonisolated-edge-core-ledger-failed",
                    "p": p,
                    "k": k,
                    "syndrome": list(syn),
                    "nonisolated_vertices": len(case_nonisolated_vertices),
                    "edge_core_count": len(case_edge_cores),
                    "edge_core_capacity": edge_core_capacity,
                }
            )
        full_support_capacity = j * edge_core_capacity + len(
            case_root_marked_boundaries
        )
        full_support_demand = j * len(active)
        full_support_ledger_slack = full_support_capacity - full_support_demand
        if full_support_ledger_slack < 0:
            raise AssertionError(
                {
                    "kind": "full-active-support-ledger-failed",
                    "p": p,
                    "k": k,
                    "syndrome": list(syn),
                    "active_complements": len(active),
                    "edge_core_count": len(case_edge_cores),
                    "root_marked_boundaries": len(case_root_marked_boundaries),
                    "full_support_capacity": full_support_capacity,
                    "full_support_demand": full_support_demand,
                    "j": j,
                }
            )
        lower_component_count = case_component_histogram["lower_core"]
        nonstar_component_ledger_slack = (
            len(case_lower_core_witnesses) - lower_component_count
        )
        if nonstar_component_ledger_slack < 0:
            raise AssertionError(
                {
                    "kind": "nonstar-component-lower-core-ledger-failed",
                    "p": p,
                    "k": k,
                    "syndrome": list(syn),
                    "lower_component_count": lower_component_count,
                    "lower_core_witness_count": len(case_lower_core_witnesses),
                }
            )
        nonisolated_ledger_slack_histogram[nonisolated_ledger_slack] += 1
        nonstar_component_ledger_slack_histogram[
            nonstar_component_ledger_slack
        ] += 1
        full_support_ledger_slack_histogram[full_support_ledger_slack] += 1
        if any(syn):
            max_nonzero_edge_core_count = max(
                max_nonzero_edge_core_count,
                len(case_edge_cores),
            )
            max_nonzero_lower_core_witness_count = max(
                max_nonzero_lower_core_witness_count,
                len(case_lower_core_witnesses),
            )
            max_nonzero_nonisolated_ledger_slack = max(
                max_nonzero_nonisolated_ledger_slack,
                nonisolated_ledger_slack,
            )
            max_nonzero_nonstar_component_ledger_slack = max(
                max_nonzero_nonstar_component_ledger_slack,
                nonstar_component_ledger_slack,
            )
            max_nonzero_full_support_ledger_slack = max(
                max_nonzero_full_support_ledger_slack,
                full_support_ledger_slack,
            )

        for plane in core_planes:
            kind, data = classify_core_plane(syn, plane["core_locator"], p)
            core_plane_histogram[kind] += 1
            pair_members = plane["pair_members"]
            added_pairs = plane["added_pairs"]
            active_positions = [
                position
                for position, index in enumerate(pair_members)
                if index in active_set
            ]
            active_pair_count = len(active_positions)
            if any(syn):
                nonzero_core_plane_histogram[kind] += 1
                nonzero_core_plane_active_pair_histogram[active_pair_count] += 1
                max_nonzero_core_plane_active_pairs = max(
                    max_nonzero_core_plane_active_pairs,
                    active_pair_count,
                )

            if kind == "empty_inconsistent":
                if active_pair_count:
                    raise AssertionError(
                        {
                            "kind": "inconsistent-core-plane-has-active-pairs",
                            "p": p,
                            "k": k,
                            "syndrome": list(syn),
                            "core": list(plane["core"]),
                            "active_pair_count": active_pair_count,
                        }
                    )
            elif kind == "point":
                if active_pair_count > 1:
                    raise AssertionError(
                        {
                            "kind": "point-core-plane-has-multiple-active-pairs",
                            "p": p,
                            "k": k,
                            "syndrome": list(syn),
                            "core": list(plane["core"]),
                            "active_pair_count": active_pair_count,
                        }
                    )
            elif kind == "full_plane":
                expected_count = len(pair_members)
                if active_pair_count != expected_count:
                    raise AssertionError(
                        {
                            "kind": "full-core-plane-missing-active-pairs",
                            "p": p,
                            "k": k,
                            "syndrome": list(syn),
                            "core": list(plane["core"]),
                            "active_pair_count": active_pair_count,
                            "expected_count": expected_count,
                        }
                    )
                if not hankel_annihilates(syn, plane["core_locator"], t + 2, p):
                    raise AssertionError(
                        {
                            "kind": "full-core-plane-lower-hankel-lift-failed",
                            "p": p,
                            "k": k,
                            "syndrome": list(syn),
                            "core": list(plane["core"]),
                        }
                    )
            elif kind == "fixed_root_line":
                root_index = next(
                    (index for index, value in enumerate(domain) if value == data["root"]),
                    None,
                )
                if active_pair_count >= 2:
                    if root_index is None:
                        raise AssertionError(
                            {
                                "kind": "fixed-root-line-root-not-in-domain",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "core": list(plane["core"]),
                                "root": data["root"],
                            }
                        )
                    for position in active_positions:
                        if root_index not in added_pairs[position]:
                            raise AssertionError(
                                {
                                    "kind": "fixed-root-line-without-common-root",
                                    "p": p,
                                    "k": k,
                                    "syndrome": list(syn),
                                    "core": list(plane["core"]),
                                    "root": data["root"],
                                    "added_pair": list(added_pairs[position]),
                                }
                            )
            elif kind in {"fixed_sum_line", "product_mobius_line"}:
                raise AssertionError(
                    {
                        "kind": "unexpected-nonfixed-same-slope-core-plane",
                        "p": p,
                        "k": k,
                        "line_kind": kind,
                        "syndrome": list(syn),
                        "core": list(plane["core"]),
                        "active_pair_count": active_pair_count,
                    }
                )
            else:
                raise AssertionError({"kind": "unknown-core-plane-kind", "value": kind})

        for top in itertools.combinations(range(n), j + 1):
            top_set = set(top)
            top_members = [
                index
                for index, complement in enumerate(complements)
                if set(complement).issubset(top_set)
            ]
            if len(top_members) != j + 1:
                raise AssertionError(
                    {
                        "kind": "unexpected-top-member-count",
                        "p": p,
                        "k": k,
                        "top": list(top),
                        "member_count": len(top_members),
                    }
                )
            if not all(index in active_set for index in top_members):
                if any(syn):
                    active_size = sum(1 for index in top_members if index in active_set)
                    max_nonzero_top_active_members = max(
                        max_nonzero_top_active_members,
                        active_size,
                    )
                    nonzero_top_active_size_histogram[active_size] += 1
                    if active_size > j:
                        raise AssertionError(
                            {
                                "kind": "nonzero-top-active-size-exceeds-j",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "top": list(top),
                                "active_size": active_size,
                                "j": j,
                            }
                        )
                continue
            full_top_cliques += 1
            if any(syn):
                nonzero_full_top_cliques += 1
                raise AssertionError(
                    {
                        "kind": "nonzero-full-top-clique",
                        "p": p,
                        "k": k,
                        "syndrome": list(syn),
                        "top": list(top),
                        "complements": [list(complements[index]) for index in top_members],
                    }
                )
            if len(full_top_examples) < max_examples:
                full_top_examples.append(
                    {
                        "syndrome": list(syn),
                        "top": list(top),
                        "complements": [list(complements[index]) for index in top_members],
                    }
                )

    return {
        "status": "PASS",
        "params": {
            "p": p,
            "n": n,
            "k": k,
            "a": a,
            "t": t,
            "j": j,
            "r": r,
            "domain": domain,
            "support_count": len(support_hankels),
            "syndrome_count": syndrome_count,
        },
        "max_active_complements": max_active,
        "max_one_exchange_edges_per_syndrome": max_edges,
        "max_triangles_per_syndrome": max_triangles,
        "max_nonzero_core_plane_active_pairs": max_nonzero_core_plane_active_pairs,
        "max_nonzero_star_corners_per_syndrome": max_nonzero_star_corners_per_syndrome,
        "max_nonzero_lower_core_corners_per_syndrome": (
            max_nonzero_lower_core_corners_per_syndrome
        ),
        "max_nonzero_star_component_size": max_nonzero_star_component_size,
        "max_nonzero_lower_core_component_size": (
            max_nonzero_lower_core_component_size
        ),
        "max_nonzero_edge_core_count": max_nonzero_edge_core_count,
        "max_nonzero_lower_core_witness_count": max_nonzero_lower_core_witness_count,
        "max_nonzero_nonisolated_ledger_slack": (
            max_nonzero_nonisolated_ledger_slack
        ),
        "max_nonzero_nonstar_component_ledger_slack": (
            max_nonzero_nonstar_component_ledger_slack
        ),
        "max_nonzero_isolated_vertices": max_nonzero_isolated_vertices,
        "max_nonzero_root_marked_boundary_count": (
            max_nonzero_root_marked_boundary_count
        ),
        "max_nonzero_first_boundary_zero_core_count": (
            max_nonzero_first_boundary_zero_core_count
        ),
        "max_nonzero_fixed_root_active_count": (
            max_nonzero_fixed_root_active_count
        ),
        "max_nonzero_fixed_root_difference_kernel_count": (
            max_nonzero_fixed_root_difference_kernel_count
        ),
        "max_nonzero_root_marked_per_root": max_nonzero_root_marked_per_root,
        "max_nonzero_root_marked_single_row_count": (
            max_nonzero_root_marked_single_row_count
        ),
        "max_nonzero_root_marked_slice_edges": (
            max_nonzero_root_marked_slice_edges
        ),
        "max_nonzero_root_marked_edge_core_count": (
            max_nonzero_root_marked_edge_core_count
        ),
        "max_nonzero_root_marked_edge_core_slack": (
            max_nonzero_root_marked_edge_core_slack
        ),
        "max_nonzero_root_marked_isolated_count": (
            max_nonzero_root_marked_isolated_count
        ),
        "max_nonzero_residual_boundary_count": (
            max_nonzero_residual_boundary_count
        ),
        "max_nonzero_residual_boundary_slack": (
            max_nonzero_residual_boundary_slack
        ),
        "iterated_difference_checks": iterated_difference_checks,
        "max_iterated_difference_chain_length": (
            max_iterated_difference_chain_length
        ),
        "iterated_boundary_identity_checks": iterated_boundary_identity_checks,
        "fixed_root_filtration_pair_checks": fixed_root_filtration_pair_checks,
        "filtration_path_checks": filtration_path_checks,
        "filtration_zero_stop_paths": filtration_zero_stop_paths,
        "filtration_terminal_paths": filtration_terminal_paths,
        "filtration_nonzero_scalar_steps": filtration_nonzero_scalar_steps,
        "terminal_bottom_support_checks": terminal_bottom_support_checks,
        "terminal_support_bound_capacity": terminal_support_bound_capacity,
        "terminal_tree_recursion_checks": terminal_tree_recursion_checks,
        "terminal_tree_branch_vertices": terminal_tree_branch_vertices,
        "terminal_tree_branch_pair_checks": terminal_tree_branch_pair_checks,
        "terminal_tree_productive_branch_pairs": (
            terminal_tree_productive_branch_pairs
        ),
        "terminal_tree_mode_packet_checks": terminal_tree_mode_packet_checks,
        "terminal_tree_productive_mode_packets": (
            terminal_tree_productive_mode_packets
        ),
        "terminal_tree_mode_anchor_reconstruction_checks": (
            terminal_tree_mode_anchor_reconstruction_checks
        ),
        "terminal_tree_productive_mode_anchor_reconstruction_checks": (
            terminal_tree_productive_mode_anchor_reconstruction_checks
        ),
        "terminal_tree_visible_packet_labels": (
            terminal_tree_visible_packet_labels
        ),
        "terminal_tree_productive_visible_packet_labels": (
            terminal_tree_productive_visible_packet_labels
        ),
        "terminal_tree_visible_packet_repeated_labels": (
            terminal_tree_visible_packet_repeated_labels
        ),
        "terminal_tree_productive_visible_packet_repeated_labels": (
            terminal_tree_productive_visible_packet_repeated_labels
        ),
        "terminal_tree_visible_packet_excess_productions": (
            terminal_tree_visible_packet_excess_productions
        ),
        "terminal_tree_productive_visible_packet_excess_productions": (
            terminal_tree_productive_visible_packet_excess_productions
        ),
        "terminal_tree_visible_packet_max_fiber_size": (
            terminal_tree_visible_packet_max_fiber_size
        ),
        "terminal_tree_productive_visible_packet_max_fiber_size": (
            terminal_tree_productive_visible_packet_max_fiber_size
        ),
        "terminal_tree_anchor_base_image_checks": (
            terminal_tree_anchor_base_image_checks
        ),
        "terminal_tree_productive_anchor_base_image_checks": (
            terminal_tree_productive_anchor_base_image_checks
        ),
        "terminal_tree_anchor_base_kernel_checks": (
            terminal_tree_anchor_base_kernel_checks
        ),
        "terminal_tree_productive_anchor_base_kernel_checks": (
            terminal_tree_productive_anchor_base_kernel_checks
        ),
        "terminal_tree_anchor_base_one_exchange_core_checks": (
            terminal_tree_anchor_base_one_exchange_core_checks
        ),
        "terminal_tree_productive_anchor_base_one_exchange_core_checks": (
            terminal_tree_productive_anchor_base_one_exchange_core_checks
        ),
        "terminal_tree_anchor_base_one_exchange_kernel_hits": (
            terminal_tree_anchor_base_one_exchange_kernel_hits
        ),
        "terminal_tree_productive_anchor_base_one_exchange_kernel_hits": (
            terminal_tree_productive_anchor_base_one_exchange_kernel_hits
        ),
        "terminal_tree_anchor_split_support_checks": (
            terminal_tree_anchor_split_support_checks
        ),
        "terminal_tree_productive_anchor_split_support_checks": (
            terminal_tree_productive_anchor_split_support_checks
        ),
        "terminal_tree_anchor_split_boundary_checks": (
            terminal_tree_anchor_split_boundary_checks
        ),
        "terminal_tree_productive_anchor_split_boundary_checks": (
            terminal_tree_productive_anchor_split_boundary_checks
        ),
        "terminal_tree_anchor_split_roundtrip_checks": (
            terminal_tree_anchor_split_roundtrip_checks
        ),
        "terminal_tree_productive_anchor_split_roundtrip_checks": (
            terminal_tree_productive_anchor_split_roundtrip_checks
        ),
        "terminal_tree_anchor_split_absorption_checks": (
            terminal_tree_anchor_split_absorption_checks
        ),
        "terminal_tree_productive_anchor_split_absorption_checks": (
            terminal_tree_productive_anchor_split_absorption_checks
        ),
        "terminal_tree_anchor_split_proper_absorption_checks": (
            terminal_tree_anchor_split_proper_absorption_checks
        ),
        "terminal_tree_productive_anchor_split_proper_absorption_checks": (
            terminal_tree_productive_anchor_split_proper_absorption_checks
        ),
        "terminal_tree_anchor_split_ordered_mode_flags": (
            terminal_tree_anchor_split_ordered_mode_flags
        ),
        "terminal_tree_productive_anchor_split_ordered_mode_flags": (
            terminal_tree_productive_anchor_split_ordered_mode_flags
        ),
        "terminal_tree_total_split_support_fiber_checks": (
            terminal_tree_total_split_support_fiber_checks
        ),
        "terminal_tree_productive_total_split_support_fiber_checks": (
            terminal_tree_productive_total_split_support_fiber_checks
        ),
        "terminal_tree_total_split_support_fiber_labels": (
            terminal_tree_total_split_support_fiber_labels
        ),
        "terminal_tree_productive_total_split_support_fiber_labels": (
            terminal_tree_productive_total_split_support_fiber_labels
        ),
        "terminal_tree_total_split_support_fiber_max_size": (
            terminal_tree_total_split_support_fiber_max_size
        ),
        "terminal_tree_productive_total_split_support_fiber_max_size": (
            terminal_tree_productive_total_split_support_fiber_max_size
        ),
        "terminal_tree_total_split_support_factorization_checks": (
            terminal_tree_total_split_support_factorization_checks
        ),
        "terminal_tree_productive_total_split_support_factorization_checks": (
            terminal_tree_productive_total_split_support_factorization_checks
        ),
        "terminal_tree_total_split_support_max_marked_roots": (
            terminal_tree_total_split_support_max_marked_roots
        ),
        "terminal_tree_productive_total_split_support_max_marked_roots": (
            terminal_tree_productive_total_split_support_max_marked_roots
        ),
        "terminal_tree_marked_exit_cube_support_checks": (
            terminal_tree_marked_exit_cube_support_checks
        ),
        "terminal_tree_productive_marked_exit_cube_support_checks": (
            terminal_tree_productive_marked_exit_cube_support_checks
        ),
        "terminal_tree_marked_exit_cube_face_checks": (
            terminal_tree_marked_exit_cube_face_checks
        ),
        "terminal_tree_productive_marked_exit_cube_face_checks": (
            terminal_tree_productive_marked_exit_cube_face_checks
        ),
        "terminal_tree_marked_exit_cube_ordered_flags": (
            terminal_tree_marked_exit_cube_ordered_flags
        ),
        "terminal_tree_productive_marked_exit_cube_ordered_flags": (
            terminal_tree_productive_marked_exit_cube_ordered_flags
        ),
        "terminal_tree_marked_exit_cube_max_marked_roots": (
            terminal_tree_marked_exit_cube_max_marked_roots
        ),
        "terminal_tree_productive_marked_exit_cube_max_marked_roots": (
            terminal_tree_productive_marked_exit_cube_max_marked_roots
        ),
        "terminal_tree_marked_core_fiber_checks": (
            terminal_tree_marked_core_fiber_checks
        ),
        "terminal_tree_productive_marked_core_fiber_checks": (
            terminal_tree_productive_marked_core_fiber_checks
        ),
        "terminal_tree_marked_core_fiber_labels": (
            terminal_tree_marked_core_fiber_labels
        ),
        "terminal_tree_productive_marked_core_fiber_labels": (
            terminal_tree_productive_marked_core_fiber_labels
        ),
        "terminal_tree_marked_core_fiber_max_size": (
            terminal_tree_marked_core_fiber_max_size
        ),
        "terminal_tree_productive_marked_core_fiber_max_size": (
            terminal_tree_productive_marked_core_fiber_max_size
        ),
        "terminal_tree_marked_core_nonempty_boundary_checks": (
            terminal_tree_marked_core_nonempty_boundary_checks
        ),
        "terminal_tree_productive_marked_core_nonempty_boundary_checks": (
            terminal_tree_productive_marked_core_nonempty_boundary_checks
        ),
        "terminal_tree_marked_core_nonempty_boundary_max_size": (
            terminal_tree_marked_core_nonempty_boundary_max_size
        ),
        "terminal_tree_productive_marked_core_nonempty_boundary_max_size": (
            terminal_tree_productive_marked_core_nonempty_boundary_max_size
        ),
        "terminal_tree_empty_core_boundary_fiber_checks": (
            terminal_tree_empty_core_boundary_fiber_checks
        ),
        "terminal_tree_productive_empty_core_boundary_fiber_checks": (
            terminal_tree_productive_empty_core_boundary_fiber_checks
        ),
        "terminal_tree_empty_core_boundary_fiber_labels": (
            terminal_tree_empty_core_boundary_fiber_labels
        ),
        "terminal_tree_productive_empty_core_boundary_fiber_labels": (
            terminal_tree_productive_empty_core_boundary_fiber_labels
        ),
        "terminal_tree_empty_core_boundary_fiber_max_size": (
            terminal_tree_empty_core_boundary_fiber_max_size
        ),
        "terminal_tree_productive_empty_core_boundary_fiber_max_size": (
            terminal_tree_productive_empty_core_boundary_fiber_max_size
        ),
        "terminal_tree_empty_core_boundary_root_linear_checks": (
            terminal_tree_empty_core_boundary_root_linear_checks
        ),
        "terminal_tree_productive_empty_core_boundary_root_linear_checks": (
            terminal_tree_productive_empty_core_boundary_root_linear_checks
        ),
        "terminal_tree_empty_core_boundary_root_linear_hits": (
            terminal_tree_empty_core_boundary_root_linear_hits
        ),
        "terminal_tree_productive_empty_core_boundary_root_linear_hits": (
            terminal_tree_productive_empty_core_boundary_root_linear_hits
        ),
        "terminal_tree_empty_core_boundary_complement_pair_checks": (
            terminal_tree_empty_core_boundary_complement_pair_checks
        ),
        "terminal_tree_productive_empty_core_boundary_complement_pair_checks": (
            terminal_tree_productive_empty_core_boundary_complement_pair_checks
        ),
        "terminal_tree_moment_complete_core_checks": (
            terminal_tree_moment_complete_core_checks
        ),
        "terminal_tree_productive_moment_complete_core_checks": (
            terminal_tree_productive_moment_complete_core_checks
        ),
        "terminal_tree_moment_complete_core_max_fiber_size": (
            terminal_tree_moment_complete_core_max_fiber_size
        ),
        "terminal_tree_productive_moment_complete_core_max_fiber_size": (
            terminal_tree_productive_moment_complete_core_max_fiber_size
        ),
        "terminal_tree_deficit_packing_core_checks": (
            terminal_tree_deficit_packing_core_checks
        ),
        "terminal_tree_productive_deficit_packing_core_checks": (
            terminal_tree_productive_deficit_packing_core_checks
        ),
        "terminal_tree_deficit_packing_core_max_deficit": (
            terminal_tree_deficit_packing_core_max_deficit
        ),
        "terminal_tree_productive_deficit_packing_core_max_deficit": (
            terminal_tree_productive_deficit_packing_core_max_deficit
        ),
        "terminal_tree_deficit_packing_core_max_fiber_size": (
            terminal_tree_deficit_packing_core_max_fiber_size
        ),
        "terminal_tree_productive_deficit_packing_core_max_fiber_size": (
            terminal_tree_productive_deficit_packing_core_max_fiber_size
        ),
        "terminal_tree_deficit_anchor_label_checks": (
            terminal_tree_deficit_anchor_label_checks
        ),
        "terminal_tree_productive_deficit_anchor_label_checks": (
            terminal_tree_productive_deficit_anchor_label_checks
        ),
        "terminal_tree_deficit_anchor_max_labels_per_fiber": (
            terminal_tree_deficit_anchor_max_labels_per_fiber
        ),
        "terminal_tree_productive_deficit_anchor_max_labels_per_fiber": (
            terminal_tree_productive_deficit_anchor_max_labels_per_fiber
        ),
        "terminal_tree_deficit_anchor_kernel_checks": (
            terminal_tree_deficit_anchor_kernel_checks
        ),
        "terminal_tree_productive_deficit_anchor_kernel_checks": (
            terminal_tree_productive_deficit_anchor_kernel_checks
        ),
        "terminal_tree_deficit_anchor_max_residual_size": (
            terminal_tree_deficit_anchor_max_residual_size
        ),
        "terminal_tree_productive_deficit_anchor_max_residual_size": (
            terminal_tree_productive_deficit_anchor_max_residual_size
        ),
        "terminal_tree_deficit_anchor_residual_fiber_checks": (
            terminal_tree_deficit_anchor_residual_fiber_checks
        ),
        "terminal_tree_productive_deficit_anchor_residual_fiber_checks": (
            terminal_tree_productive_deficit_anchor_residual_fiber_checks
        ),
        "terminal_tree_deficit_anchor_residual_fiber_labels": (
            terminal_tree_deficit_anchor_residual_fiber_labels
        ),
        "terminal_tree_productive_deficit_anchor_residual_fiber_labels": (
            terminal_tree_productive_deficit_anchor_residual_fiber_labels
        ),
        "terminal_tree_deficit_anchor_residual_fiber_max_size": (
            terminal_tree_deficit_anchor_residual_fiber_max_size
        ),
        "terminal_tree_productive_deficit_anchor_residual_fiber_max_size": (
            terminal_tree_productive_deficit_anchor_residual_fiber_max_size
        ),
        "terminal_tree_deficit_anchor_residual_fiber_max_direction": (
            terminal_tree_deficit_anchor_residual_fiber_max_direction
        ),
        "terminal_tree_productive_deficit_anchor_residual_fiber_max_direction": (
            terminal_tree_productive_deficit_anchor_residual_fiber_max_direction
        ),
        "terminal_tree_deficit_anchor_line_kernel_checks": (
            terminal_tree_deficit_anchor_line_kernel_checks
        ),
        "terminal_tree_productive_deficit_anchor_line_kernel_checks": (
            terminal_tree_productive_deficit_anchor_line_kernel_checks
        ),
        "terminal_tree_deficit_anchor_line_kernel_max_direction_roots": (
            terminal_tree_deficit_anchor_line_kernel_max_direction_roots
        ),
        "terminal_tree_productive_deficit_anchor_line_kernel_max_direction_roots": (
            terminal_tree_productive_deficit_anchor_line_kernel_max_direction_roots
        ),
        "terminal_tree_deficit_anchor_line_kernel_max_sharp_bound": (
            terminal_tree_deficit_anchor_line_kernel_max_sharp_bound
        ),
        "terminal_tree_productive_deficit_anchor_line_kernel_max_sharp_bound": (
            terminal_tree_productive_deficit_anchor_line_kernel_max_sharp_bound
        ),
        "terminal_tree_deficit_anchor_direction_mds_checks": (
            terminal_tree_deficit_anchor_direction_mds_checks
        ),
        "terminal_tree_productive_deficit_anchor_direction_mds_checks": (
            terminal_tree_productive_deficit_anchor_direction_mds_checks
        ),
        "terminal_tree_deficit_anchor_direction_mds_bad_subsets": (
            terminal_tree_deficit_anchor_direction_mds_bad_subsets
        ),
        "terminal_tree_productive_deficit_anchor_direction_mds_bad_subsets": (
            terminal_tree_productive_deficit_anchor_direction_mds_bad_subsets
        ),
        "terminal_tree_deficit_anchor_direction_mds_max_bad_subsets": (
            terminal_tree_deficit_anchor_direction_mds_max_bad_subsets
        ),
        "terminal_tree_productive_deficit_anchor_direction_mds_max_bad_subsets": (
            terminal_tree_productive_deficit_anchor_direction_mds_max_bad_subsets
        ),
        "terminal_tree_deficit_anchor_direction_mds_max_bound": (
            terminal_tree_deficit_anchor_direction_mds_max_bound
        ),
        "terminal_tree_productive_deficit_anchor_direction_mds_max_bound": (
            terminal_tree_productive_deficit_anchor_direction_mds_max_bound
        ),
        "terminal_tree_deficit_anchor_root_slice_checks": (
            terminal_tree_deficit_anchor_root_slice_checks
        ),
        "terminal_tree_productive_deficit_anchor_root_slice_checks": (
            terminal_tree_productive_deficit_anchor_root_slice_checks
        ),
        "terminal_tree_deficit_anchor_root_slice_labels": (
            terminal_tree_deficit_anchor_root_slice_labels
        ),
        "terminal_tree_productive_deficit_anchor_root_slice_labels": (
            terminal_tree_productive_deficit_anchor_root_slice_labels
        ),
        "terminal_tree_deficit_anchor_root_slice_bad_labels": (
            terminal_tree_deficit_anchor_root_slice_bad_labels
        ),
        "terminal_tree_productive_deficit_anchor_root_slice_bad_labels": (
            terminal_tree_productive_deficit_anchor_root_slice_bad_labels
        ),
        "terminal_tree_deficit_anchor_root_slice_max_bad_per_anchor": (
            terminal_tree_deficit_anchor_root_slice_max_bad_per_anchor
        ),
        "terminal_tree_productive_deficit_anchor_root_slice_max_bad_per_anchor": (
            terminal_tree_productive_deficit_anchor_root_slice_max_bad_per_anchor
        ),
        "terminal_tree_deficit_anchor_endpoint_rank_checks": (
            terminal_tree_deficit_anchor_endpoint_rank_checks
        ),
        "terminal_tree_productive_deficit_anchor_endpoint_rank_checks": (
            terminal_tree_productive_deficit_anchor_endpoint_rank_checks
        ),
        "terminal_tree_deficit_anchor_endpoint_rank_defects": (
            terminal_tree_deficit_anchor_endpoint_rank_defects
        ),
        "terminal_tree_productive_deficit_anchor_endpoint_rank_defects": (
            terminal_tree_productive_deficit_anchor_endpoint_rank_defects
        ),
        "terminal_tree_deficit_anchor_endpoint_rank_max_defect": (
            terminal_tree_deficit_anchor_endpoint_rank_max_defect
        ),
        "terminal_tree_productive_deficit_anchor_endpoint_rank_max_defect": (
            terminal_tree_productive_deficit_anchor_endpoint_rank_max_defect
        ),
        "terminal_tree_core_packet_checks": (
            terminal_tree_core_packet_checks
        ),
        "terminal_tree_productive_core_packet_checks": (
            terminal_tree_productive_core_packet_checks
        ),
        "terminal_tree_core_simple_pole_lift_checks": (
            terminal_tree_core_simple_pole_lift_checks
        ),
        "terminal_tree_productive_core_simple_pole_lift_checks": (
            terminal_tree_productive_core_simple_pole_lift_checks
        ),
        "terminal_tree_unmarked_zero_cube_support_checks": (
            terminal_tree_unmarked_zero_cube_support_checks
        ),
        "terminal_tree_productive_unmarked_zero_cube_support_checks": (
            terminal_tree_productive_unmarked_zero_cube_support_checks
        ),
        "terminal_tree_unmarked_zero_cube_face_checks": (
            terminal_tree_unmarked_zero_cube_face_checks
        ),
        "terminal_tree_productive_unmarked_zero_cube_face_checks": (
            terminal_tree_productive_unmarked_zero_cube_face_checks
        ),
        "terminal_tree_unmarked_zero_cube_max_unmarked_roots": (
            terminal_tree_unmarked_zero_cube_max_unmarked_roots
        ),
        "terminal_tree_productive_unmarked_zero_cube_max_unmarked_roots": (
            terminal_tree_productive_unmarked_zero_cube_max_unmarked_roots
        ),
        "terminal_tree_mixed_marked_zero_cube_support_checks": (
            terminal_tree_mixed_marked_zero_cube_support_checks
        ),
        "terminal_tree_productive_mixed_marked_zero_cube_support_checks": (
            terminal_tree_productive_mixed_marked_zero_cube_support_checks
        ),
        "terminal_tree_mixed_marked_zero_cube_face_checks": (
            terminal_tree_mixed_marked_zero_cube_face_checks
        ),
        "terminal_tree_productive_mixed_marked_zero_cube_face_checks": (
            terminal_tree_productive_mixed_marked_zero_cube_face_checks
        ),
        "terminal_tree_mixed_marked_zero_cube_max_deleted_unmarked_roots": (
            terminal_tree_mixed_marked_zero_cube_max_deleted_unmarked_roots
        ),
        "terminal_tree_productive_mixed_marked_zero_cube_max_deleted_unmarked_roots": (
            terminal_tree_productive_mixed_marked_zero_cube_max_deleted_unmarked_roots
        ),
        "terminal_tree_unmarked_shift_marking_support_checks": (
            terminal_tree_unmarked_shift_marking_support_checks
        ),
        "terminal_tree_productive_unmarked_shift_marking_support_checks": (
            terminal_tree_productive_unmarked_shift_marking_support_checks
        ),
        "terminal_tree_unmarked_shift_marking_root_checks": (
            terminal_tree_unmarked_shift_marking_root_checks
        ),
        "terminal_tree_productive_unmarked_shift_marking_root_checks": (
            terminal_tree_productive_unmarked_shift_marking_root_checks
        ),
        "terminal_tree_unmarked_shift_marking_max_deleted_roots": (
            terminal_tree_unmarked_shift_marking_max_deleted_roots
        ),
        "terminal_tree_productive_unmarked_shift_marking_max_deleted_roots": (
            terminal_tree_productive_unmarked_shift_marking_max_deleted_roots
        ),
        "terminal_tree_anchor_fiber_checks": (
            terminal_tree_anchor_fiber_checks
        ),
        "terminal_tree_productive_anchor_fiber_checks": (
            terminal_tree_productive_anchor_fiber_checks
        ),
        "terminal_tree_anchor_fiber_labels": (
            terminal_tree_anchor_fiber_labels
        ),
        "terminal_tree_productive_anchor_fiber_labels": (
            terminal_tree_productive_anchor_fiber_labels
        ),
        "terminal_tree_anchor_fiber_max_size": (
            terminal_tree_anchor_fiber_max_size
        ),
        "terminal_tree_productive_anchor_fiber_max_size": (
            terminal_tree_productive_anchor_fiber_max_size
        ),
        "terminal_tree_mode_rank_checks": terminal_tree_mode_rank_checks,
        "terminal_tree_productive_mode_rank_checks": (
            terminal_tree_productive_mode_rank_checks
        ),
        "terminal_tree_mode_peeling_checks": terminal_tree_mode_peeling_checks,
        "terminal_tree_productive_mode_peeling_checks": (
            terminal_tree_productive_mode_peeling_checks
        ),
        "terminal_tree_mode_annihilator_checks": (
            terminal_tree_mode_annihilator_checks
        ),
        "terminal_tree_productive_mode_annihilator_checks": (
            terminal_tree_productive_mode_annihilator_checks
        ),
        "terminal_tree_boundary_alias_checks": terminal_tree_boundary_alias_checks,
        "terminal_tree_productive_boundary_alias_checks": (
            terminal_tree_productive_boundary_alias_checks
        ),
        "terminal_tree_boundary_aliases": terminal_tree_boundary_aliases,
        "terminal_tree_productive_boundary_aliases": (
            terminal_tree_productive_boundary_aliases
        ),
        "terminal_tree_boundary_scalar_fit_candidate_checks": (
            terminal_tree_boundary_scalar_fit_candidate_checks
        ),
        "terminal_tree_productive_boundary_scalar_fit_candidate_checks": (
            terminal_tree_productive_boundary_scalar_fit_candidate_checks
        ),
        "terminal_tree_boundary_scalar_fits": terminal_tree_boundary_scalar_fits,
        "terminal_tree_productive_boundary_scalar_fits": (
            terminal_tree_productive_boundary_scalar_fits
        ),
        "terminal_tree_boundary_root_linear_checks": (
            terminal_tree_boundary_root_linear_checks
        ),
        "terminal_tree_productive_boundary_root_linear_checks": (
            terminal_tree_productive_boundary_root_linear_checks
        ),
        "terminal_tree_boundary_root_linear_hits": (
            terminal_tree_boundary_root_linear_hits
        ),
        "terminal_tree_productive_boundary_root_linear_hits": (
            terminal_tree_productive_boundary_root_linear_hits
        ),
        "terminal_tree_boundary_root_linear_support_count": len(
            terminal_tree_boundary_root_linear_by_support
        ),
        "terminal_tree_boundary_support_unique": (
            terminal_tree_boundary_support_unique
        ),
        "terminal_tree_productive_boundary_support_unique": (
            terminal_tree_productive_boundary_support_unique
        ),
        "terminal_tree_boundary_max_fiber_size": (
            terminal_tree_boundary_max_fiber_size
        ),
        "terminal_tree_productive_boundary_max_fiber_size": (
            terminal_tree_productive_boundary_max_fiber_size
        ),
        "terminal_tree_mode_labeled_capacity_by_size": {
            size: math.comb(n, size) * (p - 1) ** size
            for size in sorted(terminal_tree_mode_sizes_seen)
        },
        "terminal_tree_boundary_full_domain_visible_sequences": (
            terminal_tree_boundary_support_unique
            + terminal_tree_boundary_root_linear_hits // 2
        ),
        "terminal_tree_boundary_labeled_capacity_by_size": {
            size: math.comb(n, size) * (p - 1) ** size
            for size in sorted(terminal_tree_boundary_mode_sizes_seen)
        },
        "terminal_tree_boundary_image_lower_bound_by_size": {
            size: math.ceil(
                math.comb(n, size) * (p - 1) ** size / (n // size)
            )
            for size in sorted(terminal_tree_boundary_mode_sizes_seen)
        },
        "terminal_tree_multiflag_cores": terminal_tree_multiflag_cores,
        "max_iterated_boundary_chain_length": max_iterated_boundary_chain_length,
        "max_nonzero_iterated_boundary_active_cores": (
            max_nonzero_iterated_boundary_active_cores
        ),
        "max_nonzero_iterated_boundary_zero_cores": (
            max_nonzero_iterated_boundary_zero_cores
        ),
        "max_nonzero_iterated_boundary_marked": (
            max_nonzero_iterated_boundary_marked
        ),
        "max_nonzero_fixed_root_filtration_pairs": (
            max_nonzero_fixed_root_filtration_pairs
        ),
        "max_nonzero_filtration_paths": max_nonzero_filtration_paths,
        "max_nonzero_zero_stop_filtration_paths": (
            max_nonzero_zero_stop_filtration_paths
        ),
        "max_nonzero_terminal_filtration_paths": (
            max_nonzero_terminal_filtration_paths
        ),
        "max_nonzero_filtration_nonzero_scalar_steps": (
            max_nonzero_filtration_nonzero_scalar_steps
        ),
        "max_nonzero_terminal_bottom_supports": (
            max_nonzero_terminal_bottom_supports
        ),
        "max_nonzero_terminal_support_bound_slack": (
            max_nonzero_terminal_support_bound_slack
        ),
        "max_nonzero_terminal_tree_count": max_nonzero_terminal_tree_count,
        "max_nonzero_terminal_tree_branch_vertices": (
            max_nonzero_terminal_tree_branch_vertices
        ),
        "max_nonzero_terminal_tree_branch_pairs": (
            max_nonzero_terminal_tree_branch_pairs
        ),
        "max_nonzero_terminal_tree_productive_branch_pairs": (
            max_nonzero_terminal_tree_productive_branch_pairs
        ),
        "max_nonzero_terminal_tree_mode_packets": (
            max_nonzero_terminal_tree_mode_packets
        ),
        "max_nonzero_terminal_tree_productive_mode_packets": (
            max_nonzero_terminal_tree_productive_mode_packets
        ),
        "max_nonzero_terminal_tree_visible_packet_fiber_size": (
            max_nonzero_terminal_tree_visible_packet_fiber_size
        ),
        "max_nonzero_terminal_tree_productive_visible_packet_fiber_size": (
            max_nonzero_terminal_tree_productive_visible_packet_fiber_size
        ),
        "max_nonzero_terminal_tree_mode_size": (
            max_nonzero_terminal_tree_mode_size
        ),
        "max_nonzero_terminal_tree_mode_rank_checks": (
            max_nonzero_terminal_tree_mode_rank_checks
        ),
        "max_nonzero_terminal_tree_mode_rank_size": (
            max_nonzero_terminal_tree_mode_rank_size
        ),
        "max_nonzero_terminal_tree_mode_peeling_checks": (
            max_nonzero_terminal_tree_mode_peeling_checks
        ),
        "max_nonzero_terminal_tree_mode_annihilator_checks": (
            max_nonzero_terminal_tree_mode_annihilator_checks
        ),
        "max_nonzero_terminal_tree_multiflag_cores": (
            max_nonzero_terminal_tree_multiflag_cores
        ),
        "max_nonzero_isolated_marked_boundary_slack": (
            max_nonzero_isolated_marked_boundary_slack
        ),
        "max_nonzero_full_support_ledger_slack": (
            max_nonzero_full_support_ledger_slack
        ),
        "one_exchange_edges": one_exchange_edges,
        "star_triangles": star_triangles,
        "top_triangles": top_triangles,
        "nonzero_top_triangles": nonzero_top_triangles,
        "full_top_cliques": full_top_cliques,
        "nonzero_full_top_cliques": nonzero_full_top_cliques,
        "max_nonzero_top_active_members": max_nonzero_top_active_members,
        "active_complement_histogram": dict(sorted(active_histogram.items())),
        "one_exchange_edge_histogram": dict(sorted(edge_histogram.items())),
        "triangle_histogram": dict(sorted(triangle_histogram.items())),
        "core_plane_histogram": dict(sorted(core_plane_histogram.items())),
        "nonzero_core_plane_histogram": dict(
            sorted(nonzero_core_plane_histogram.items())
        ),
        "nonzero_core_plane_active_pair_histogram": dict(
            sorted(nonzero_core_plane_active_pair_histogram.items())
        ),
        "corner_histogram": dict(sorted(corner_histogram.items())),
        "nonzero_corner_histogram": dict(sorted(nonzero_corner_histogram.items())),
        "component_histogram": dict(sorted(component_histogram.items())),
        "nonzero_component_histogram": dict(
            sorted(nonzero_component_histogram.items())
        ),
        "component_size_histogram": dict(sorted(component_size_histogram.items())),
        "nonzero_component_size_histogram": dict(
            sorted(nonzero_component_size_histogram.items())
        ),
        "nonisolated_ledger_slack_histogram": dict(
            sorted(nonisolated_ledger_slack_histogram.items())
        ),
        "nonstar_component_ledger_slack_histogram": dict(
            sorted(nonstar_component_ledger_slack_histogram.items())
        ),
        "isolated_vertex_histogram": dict(sorted(isolated_vertex_histogram.items())),
        "isolated_boundary_zero_histogram": dict(
            sorted(isolated_boundary_zero_histogram.items())
        ),
        "isolated_marked_boundary_slack_histogram": dict(
            sorted(isolated_marked_boundary_slack_histogram.items())
        ),
        "full_support_ledger_slack_histogram": dict(
            sorted(full_support_ledger_slack_histogram.items())
        ),
        "first_boundary_zero_core_histogram": dict(
            sorted(first_boundary_zero_core_histogram.items())
        ),
        "first_boundary_incidence_defect_histogram": dict(
            sorted(first_boundary_incidence_defect_histogram.items())
        ),
        "fixed_root_decomposition_defect_histogram": dict(
            sorted(fixed_root_decomposition_defect_histogram.items())
        ),
        "fixed_root_difference_defect_histogram": dict(
            sorted(fixed_root_difference_defect_histogram.items())
        ),
        "root_marked_single_row_defect_histogram": dict(
            sorted(root_marked_single_row_defect_histogram.items())
        ),
        "root_marked_edge_core_slack_histogram": dict(
            sorted(root_marked_edge_core_slack_histogram.items())
        ),
        "root_marked_isolated_histogram": dict(
            sorted(root_marked_isolated_histogram.items())
        ),
        "residual_boundary_slack_histogram": dict(
            sorted(residual_boundary_slack_histogram.items())
        ),
        "iterated_difference_defect_histogram": dict(
            sorted(iterated_difference_defect_histogram.items())
        ),
        "iterated_boundary_defect_histogram": dict(
            sorted(iterated_boundary_defect_histogram.items())
        ),
        "fixed_root_filtration_defect_histogram": dict(
            sorted(fixed_root_filtration_defect_histogram.items())
        ),
        "filtration_path_defect_histogram": dict(
            sorted(filtration_path_defect_histogram.items())
        ),
        "filtration_path_partition_defect_histogram": dict(
            sorted(filtration_path_partition_defect_histogram.items())
        ),
        "filtration_zero_stop_depth_histogram": dict(
            sorted(filtration_zero_stop_depth_histogram.items())
        ),
        "terminal_support_bound_slack_histogram": dict(
            sorted(terminal_support_bound_slack_histogram.items())
        ),
        "terminal_tree_recursion_defect_histogram": dict(
            sorted(terminal_tree_recursion_defect_histogram.items())
        ),
        "terminal_tree_branch_vertex_histogram": dict(
            sorted(terminal_tree_branch_vertex_histogram.items())
        ),
        "terminal_tree_branch_pair_histogram": dict(
            sorted(terminal_tree_branch_pair_histogram.items())
        ),
        "terminal_tree_productive_branch_pair_histogram": dict(
            sorted(terminal_tree_productive_branch_pair_histogram.items())
        ),
        "terminal_tree_mode_packet_histogram": dict(
            sorted(terminal_tree_mode_packet_histogram.items())
        ),
        "terminal_tree_productive_mode_packet_histogram": dict(
            sorted(terminal_tree_productive_mode_packet_histogram.items())
        ),
        "terminal_tree_visible_packet_fiber_size_histogram": dict(
            sorted(terminal_tree_visible_packet_fiber_size_histogram.items())
        ),
        "terminal_tree_productive_visible_packet_fiber_size_histogram": dict(
            sorted(
                terminal_tree_productive_visible_packet_fiber_size_histogram.items()
            )
        ),
        "terminal_tree_mode_size_histogram": dict(
            sorted(terminal_tree_mode_size_histogram.items())
        ),
        "terminal_tree_productive_mode_size_histogram": dict(
            sorted(terminal_tree_productive_mode_size_histogram.items())
        ),
        "terminal_tree_mode_rank_histogram": dict(
            sorted(terminal_tree_mode_rank_histogram.items())
        ),
        "terminal_tree_productive_mode_rank_histogram": dict(
            sorted(terminal_tree_productive_mode_rank_histogram.items())
        ),
        "terminal_tree_mode_rank_size_histogram": dict(
            sorted(terminal_tree_mode_rank_size_histogram.items())
        ),
        "terminal_tree_mode_peeling_histogram": dict(
            sorted(terminal_tree_mode_peeling_histogram.items())
        ),
        "terminal_tree_productive_mode_peeling_histogram": dict(
            sorted(terminal_tree_productive_mode_peeling_histogram.items())
        ),
        "terminal_tree_mode_peeling_subset_size_histogram": dict(
            sorted(terminal_tree_mode_peeling_subset_size_histogram.items())
        ),
        "terminal_tree_mode_annihilator_histogram": dict(
            sorted(terminal_tree_mode_annihilator_histogram.items())
        ),
        "terminal_tree_productive_mode_annihilator_histogram": dict(
            sorted(terminal_tree_productive_mode_annihilator_histogram.items())
        ),
        "terminal_tree_mode_annihilator_size_histogram": dict(
            sorted(terminal_tree_mode_annihilator_size_histogram.items())
        ),
        "terminal_tree_boundary_alias_histogram": dict(
            sorted(terminal_tree_boundary_alias_histogram.items())
        ),
        "terminal_tree_productive_boundary_alias_histogram": dict(
            sorted(terminal_tree_productive_boundary_alias_histogram.items())
        ),
        "terminal_tree_boundary_scalar_fit_histogram": dict(
            sorted(terminal_tree_boundary_scalar_fit_histogram.items())
        ),
        "terminal_tree_productive_boundary_scalar_fit_histogram": dict(
            sorted(terminal_tree_productive_boundary_scalar_fit_histogram.items())
        ),
        "terminal_tree_boundary_root_linear_histogram": dict(
            sorted(terminal_tree_boundary_root_linear_histogram.items())
        ),
        "terminal_tree_productive_boundary_root_linear_histogram": dict(
            sorted(terminal_tree_productive_boundary_root_linear_histogram.items())
        ),
        "terminal_tree_boundary_root_linear_support_histogram": dict(
            sorted(
                Counter(terminal_tree_boundary_root_linear_by_support.values()).items()
            )
        ),
        "terminal_tree_boundary_fiber_size_histogram": dict(
            sorted(terminal_tree_boundary_fiber_size_histogram.items())
        ),
        "terminal_tree_productive_boundary_fiber_size_histogram": dict(
            sorted(terminal_tree_productive_boundary_fiber_size_histogram.items())
        ),
        "terminal_tree_multiflag_core_histogram": dict(
            sorted(terminal_tree_multiflag_core_histogram.items())
        ),
        "nonzero_top_active_size_histogram": dict(
            sorted(nonzero_top_active_size_histogram.items())
        ),
        "star_examples": star_examples,
        "top_examples": top_examples,
        "full_top_examples": full_top_examples,
    }


def parse_case(value: str) -> tuple[int, int]:
    parts = value.split(",")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("case must have form p,k")
    try:
        return (int(parts[0]), int(parts[1]))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("case entries must be integers") from exc


def print_summary(results: Sequence[dict[str, object]]) -> None:
    print("M1 t=2 Hankel triangle packet verifier")
    for result in results:
        params = result["params"]
        print(
            "case "
            f"p={params['p']} n={params['n']} k={params['k']} "
            f"a={params['a']} j={params['j']}: "
            f"syndromes={params['syndrome_count']} "
            f"edges={result['one_exchange_edges']} "
            f"star_triangles={result['star_triangles']} "
            f"top_triangles={result['top_triangles']} "
            f"nonzero_top={result['nonzero_top_triangles']} "
            f"full_top={result['full_top_cliques']} "
            f"max_nonzero_core_plane={result['max_nonzero_core_plane_active_pairs']} "
            f"max_nonzero_lower_corners="
            f"{result['max_nonzero_lower_core_corners_per_syndrome']} "
            f"max_nonzero_lower_component="
            f"{result['max_nonzero_lower_core_component_size']} "
            f"max_nonzero_edge_cores={result['max_nonzero_edge_core_count']} "
            f"max_nonzero_boundary_zero_cores="
            f"{result['max_nonzero_first_boundary_zero_core_count']} "
            f"max_nonzero_fixed_root_active="
            f"{result['max_nonzero_fixed_root_active_count']} "
            f"max_nonzero_root_difference_kernel="
            f"{result['max_nonzero_fixed_root_difference_kernel_count']} "
            f"max_nonzero_root_marked_per_root="
            f"{result['max_nonzero_root_marked_per_root']} "
            f"max_nonzero_root_marked_single_row="
            f"{result['max_nonzero_root_marked_single_row_count']} "
            f"max_nonzero_root_marked_edge_cores="
            f"{result['max_nonzero_root_marked_edge_core_count']} "
            f"max_nonzero_root_marked_isolated="
            f"{result['max_nonzero_root_marked_isolated_count']} "
            f"max_nonzero_isolated={result['max_nonzero_isolated_vertices']} "
            f"max_nonzero_marked_boundary="
            f"{result['max_nonzero_root_marked_boundary_count']} "
            f"max_nonzero_iterated_boundary_marked="
            f"{result['max_nonzero_iterated_boundary_marked']} "
            f"max_nonzero_fixed_root_filtration_pairs="
            f"{result['max_nonzero_fixed_root_filtration_pairs']} "
            f"max_nonzero_zero_stop_paths="
            f"{result['max_nonzero_zero_stop_filtration_paths']} "
            f"max_nonzero_terminal_paths="
            f"{result['max_nonzero_terminal_filtration_paths']} "
            f"max_nonzero_zero_free_steps="
            f"{result['max_nonzero_filtration_nonzero_scalar_steps']} "
            f"max_nonzero_terminal_supports="
            f"{result['max_nonzero_terminal_bottom_supports']} "
            f"max_nonzero_terminal_tree_count="
            f"{result['max_nonzero_terminal_tree_count']} "
            f"max_nonzero_terminal_tree_branches="
            f"{result['max_nonzero_terminal_tree_branch_vertices']} "
            f"max_nonzero_terminal_tree_branch_pairs="
            f"{result['max_nonzero_terminal_tree_branch_pairs']} "
            f"anchor_reconstructions="
            f"{result['terminal_tree_mode_anchor_reconstruction_checks']} "
            f"visible_packet_max_fiber="
            f"{result['max_nonzero_terminal_tree_visible_packet_fiber_size']} "
            f"visible_packet_excess="
            f"{result['terminal_tree_visible_packet_excess_productions']} "
            f"anchor_base_images="
            f"{result['terminal_tree_anchor_base_image_checks']} "
            f"anchor_base_kernel_checks="
            f"{result['terminal_tree_anchor_base_kernel_checks']} "
            f"one_exchange_anchor_core_checks="
            f"{result['terminal_tree_anchor_base_one_exchange_core_checks']} "
            f"one_exchange_anchor_kernel_hits="
            f"{result['terminal_tree_anchor_base_one_exchange_kernel_hits']} "
            f"anchor_split_supports="
            f"{result['terminal_tree_anchor_split_support_checks']} "
            f"anchor_split_boundaries="
            f"{result['terminal_tree_anchor_split_boundary_checks']} "
            f"anchor_split_roundtrips="
            f"{result['terminal_tree_anchor_split_roundtrip_checks']} "
            f"anchor_split_absorptions="
            f"{result['terminal_tree_anchor_split_absorption_checks']} "
            f"anchor_split_ordered_flags="
            f"{result['terminal_tree_anchor_split_ordered_mode_flags']} "
            f"total_split_fiber_checks="
            f"{result['terminal_tree_total_split_support_fiber_checks']} "
            f"total_split_factorizations="
            f"{result['terminal_tree_total_split_support_factorization_checks']} "
            f"marked_exit_cube_faces="
            f"{result['terminal_tree_marked_exit_cube_face_checks']} "
            f"marked_core_fiber_checks="
            f"{result['terminal_tree_marked_core_fiber_checks']} "
            f"marked_core_fiber_max="
            f"{result['terminal_tree_marked_core_fiber_max_size']} "
            f"marked_core_nonempty_boundary="
            f"{result['terminal_tree_marked_core_nonempty_boundary_checks']} "
            f"marked_core_nonempty_boundary_max="
            f"{result['terminal_tree_marked_core_nonempty_boundary_max_size']} "
            f"empty_core_boundary_fibers="
            f"{result['terminal_tree_empty_core_boundary_fiber_checks']} "
            f"empty_core_boundary_max="
            f"{result['terminal_tree_empty_core_boundary_fiber_max_size']} "
            f"empty_core_root_linear="
            f"{result['terminal_tree_empty_core_boundary_root_linear_hits']} "
            f"moment_complete_cores="
            f"{result['terminal_tree_moment_complete_core_checks']} "
            f"moment_complete_core_max="
            f"{result['terminal_tree_moment_complete_core_max_fiber_size']} "
            f"deficit_packing_cores="
            f"{result['terminal_tree_deficit_packing_core_checks']} "
            f"deficit_packing_max_d="
            f"{result['terminal_tree_deficit_packing_core_max_deficit']} "
            f"deficit_packing_max="
            f"{result['terminal_tree_deficit_packing_core_max_fiber_size']} "
            f"deficit_anchor_labels="
            f"{result['terminal_tree_deficit_anchor_label_checks']} "
            f"deficit_anchor_max="
            f"{result['terminal_tree_deficit_anchor_max_labels_per_fiber']} "
            f"deficit_anchor_kernels="
            f"{result['terminal_tree_deficit_anchor_kernel_checks']} "
            f"deficit_anchor_residual_max="
            f"{result['terminal_tree_deficit_anchor_max_residual_size']} "
            f"deficit_anchor_residual_fibers="
            f"{result['terminal_tree_deficit_anchor_residual_fiber_checks']} "
            f"deficit_anchor_residual_fiber_max="
            f"{result['terminal_tree_deficit_anchor_residual_fiber_max_size']} "
            f"deficit_anchor_residual_dim_max="
            f"{result['terminal_tree_deficit_anchor_residual_fiber_max_direction']} "
            f"deficit_anchor_line_kernels="
            f"{result['terminal_tree_deficit_anchor_line_kernel_checks']} "
            f"deficit_anchor_line_kernel_root_max="
            f"{result['terminal_tree_deficit_anchor_line_kernel_max_direction_roots']} "
            f"deficit_anchor_direction_mds="
            f"{result['terminal_tree_deficit_anchor_direction_mds_checks']} "
            f"deficit_anchor_direction_mds_bad_max="
            f"{result['terminal_tree_deficit_anchor_direction_mds_max_bad_subsets']} "
            f"deficit_anchor_root_slices="
            f"{result['terminal_tree_deficit_anchor_root_slice_checks']} "
            f"deficit_anchor_root_slice_bad="
            f"{result['terminal_tree_deficit_anchor_root_slice_bad_labels']} "
            f"deficit_anchor_endpoint_rank_checks="
            f"{result['terminal_tree_deficit_anchor_endpoint_rank_checks']} "
            f"deficit_anchor_endpoint_rank_defects="
            f"{result['terminal_tree_deficit_anchor_endpoint_rank_defects']} "
            f"core_packets={result['terminal_tree_core_packet_checks']} "
            f"core_simple_pole_lifts="
            f"{result['terminal_tree_core_simple_pole_lift_checks']} "
            f"unmarked_zero_cube_faces="
            f"{result['terminal_tree_unmarked_zero_cube_face_checks']} "
            f"mixed_cube_faces="
            f"{result['terminal_tree_mixed_marked_zero_cube_face_checks']} "
            f"unmarked_shift_roots="
            f"{result['terminal_tree_unmarked_shift_marking_root_checks']} "
            f"anchor_fiber_checks="
            f"{result['terminal_tree_anchor_fiber_checks']} "
            f"anchor_fiber_max="
            f"{result['terminal_tree_anchor_fiber_max_size']} "
            f"max_nonzero_terminal_tree_mode_size="
            f"{result['max_nonzero_terminal_tree_mode_size']} "
            f"max_nonzero_terminal_tree_mode_rank_size="
            f"{result['max_nonzero_terminal_tree_mode_rank_size']} "
            f"max_nonzero_terminal_tree_mode_peeling="
            f"{result['max_nonzero_terminal_tree_mode_peeling_checks']} "
            f"max_nonzero_terminal_tree_mode_annihilator="
            f"{result['max_nonzero_terminal_tree_mode_annihilator_checks']} "
            f"boundary_alias_checks="
            f"{result['terminal_tree_boundary_alias_checks']} "
            f"boundary_aliases={result['terminal_tree_boundary_aliases']} "
            f"boundary_scalar_fits="
            f"{result['terminal_tree_boundary_scalar_fits']} "
            f"boundary_root_linear="
            f"{result['terminal_tree_boundary_root_linear_hits']} "
            f"boundary_support_unique="
            f"{result['terminal_tree_boundary_support_unique']} "
            f"boundary_visible_sequences="
            f"{result['terminal_tree_boundary_full_domain_visible_sequences']} "
            f"boundary_max_fiber="
            f"{result['terminal_tree_boundary_max_fiber_size']} "
            f"max_nonzero_full_support_slack="
            f"{result['max_nonzero_full_support_ledger_slack']} "
            f"max_nonzero_top_active={result['max_nonzero_top_active_members']}"
        )
    print("PASS")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        action="append",
        type=parse_case,
        dest="cases",
        help="case p,k with t fixed to 2; may be supplied multiple times",
    )
    parser.add_argument(
        "--max-syndromes",
        type=int,
        default=100_000,
        help="guardrail for exact syndrome enumeration",
    )
    parser.add_argument(
        "--max-examples",
        type=int,
        default=3,
        help="number of star/top examples retained",
    )
    parser.add_argument("--json", action="store_true", help="print JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cases = args.cases or [(5, 1), (7, 1), (7, 2), (7, 3)]
    results = [
        analyze_case(
            p=p,
            k=k,
            max_syndromes=args.max_syndromes,
            max_examples=args.max_examples,
        )
        for p, k in cases
    ]
    if args.json:
        print(json.dumps({"status": "PASS", "cases": results}, indent=2, sort_keys=True))
    else:
        print_summary(results)


if __name__ == "__main__":
    main()
