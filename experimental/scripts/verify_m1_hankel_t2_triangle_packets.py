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
            nonlocal terminal_tree_multiflag_cores
            nonlocal max_nonzero_terminal_bottom_supports
            nonlocal max_nonzero_terminal_support_bound_slack
            nonlocal max_nonzero_terminal_tree_count
            nonlocal max_nonzero_terminal_tree_branch_vertices
            nonlocal max_nonzero_terminal_tree_branch_pairs
            nonlocal max_nonzero_terminal_tree_productive_branch_pairs
            nonlocal max_nonzero_terminal_tree_mode_packets
            nonlocal max_nonzero_terminal_tree_productive_mode_packets
            nonlocal max_nonzero_terminal_tree_mode_size
            nonlocal max_nonzero_terminal_tree_mode_rank_checks
            nonlocal max_nonzero_terminal_tree_mode_rank_size
            nonlocal max_nonzero_terminal_tree_mode_peeling_checks
            nonlocal max_nonzero_terminal_tree_mode_annihilator_checks
            nonlocal max_nonzero_terminal_tree_multiflag_cores

            terminal_supports: set[tuple[int, ...]] = set()
            terminal_paths_by_core: Counter[tuple[int, ...]] = Counter()
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
                            if productive_children >= 2:
                                terminal_tree_productive_boundary_alias_checks += 1
                                terminal_tree_productive_boundary_aliases += (
                                    len(aliases)
                                )
                                terminal_tree_productive_boundary_alias_histogram[
                                    len(aliases)
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
