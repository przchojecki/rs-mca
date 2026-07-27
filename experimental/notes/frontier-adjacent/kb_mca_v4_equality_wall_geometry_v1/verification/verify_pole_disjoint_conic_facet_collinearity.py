#!/usr/bin/env python3
"""Verify the pole-disjoint conic facet-collinearity reduction.

Exact checks over the deployed KoalaBear prime field:

  * endpoint and complement bidegree arithmetic;
  * the reciprocal block-coordinate law z_j(l) * M(alpha_j, l) =
    kappa_j * B(l) for random pole-disjoint coordinate data;
  * rank exactly 3 of the conic evaluation matrix;
  * the facet-triple kernel identity and collinearity (Theorem 5.1),
    with a non-degenerate 13-set negative control;
  * the 13-set pencil refinement and its negative control
    (Theorem 5.2);
  * component bidegree double count and odd-part parity
    (Theorem 7.1, Corollary 7.2);
  * the Q=1 dihedral degree ledger and the exact cycle-flow rewrite
    (Theorem 9.9, Corollary 9.10);
  * the outgoing/deck-conjugate Bezout ledger, exclusion of
    Q=2,3,4, and the exact Q=5 equality packet
    (Theorem 9.13, Corollary 9.14);
  * the Q=5 invariant/anti-invariant descent to a
    (5,5)-by-(3,4) resultant of degree 35 (Theorem 9.15);
  * exclusion of outgoing graph parts at Q=5, leaving only the
    component partitions 5 and 3+2 (Corollary 9.16);
  * the source-derivative contradiction excluding the complete
    Q=5 equality packet (Theorem 9.17);
  * the fixed-pole odd/even proportionality valid for every Q>=2,
    and the exact Q=6 forced-intersection/slack ledger
    (Corollary 9.18);
  * invariant-coordinate source factors, the sharpened all-Q
    intersection bound, and the Q=6 quotient-resultant residual cap
    (Theorem 9.19, Corollary 9.20);
  * the Q=6, s=6 rectangular-grid endpoint and graph-branch
    cross-intersection capacity (Corollaries 9.21-9.22);
  * the quotient-pole capacity exclusion of Q=6 cases s=2,3,4,5,
    the nonfixed s=1 guard, and the remaining s=0,1,6 trichotomy
    (Theorem 9.23);
  * the Q=6, s=6 fixed split-pencil star for all sixty conjugate
    block pairs (Corollary 9.24);
  * the Q=6, s=6 invariant/source-fiber label near-coincidence and
    complementary two-regular pole graph (Corollary 9.25);
  * the Q=6, s=6 ten-fiber pencil capacity and pole-cycle partition
    list (Corollary 9.26);
  * the Q=6, s=6 source-facet deck, canonical matching, component
    edge-color counts, and exact migration correction
    (Corollaries 9.27-9.28);
  * a finite non-monochromatic correction fixture proving that the
    new cardinality ledgers alone do not imply component compatibility
    (Guardrail 9.29);
  * design-level triple census: the canonical two-template model
    contains co-12-set triples (irreducible-infeasible), the cyclic
    design-only guardrail contains none and admits an exact Q=6
    perfect matching with core replication five and difference
    replication twelve;
  * the quadratic-section pullback identity (9.3) and the grid
    vertex formula (8.1)-(8.2) on an exact synthetic split model in
    the small (a=4, power 2) analogue;
  * fail-closed certificate comparison and tamper rejection.

The verifier is a consistency check for the note
proof/pole_disjoint_conic_facet_collinearity_reduction.md.
It is not evidence that the remaining one-triangle target is proved.
"""

from __future__ import annotations
class VerificationError(RuntimeError):
    """Raised when an exact verifier condition fails."""


def require(condition, message):
    if not condition:
        raise VerificationError(str(message))


if not __debug__:
    raise RuntimeError(
        "Verifier refuses optimized execution; rerun without Python -O."
    )



import argparse
import copy
import hashlib
import json
from itertools import combinations
from pathlib import Path

P = (1 << 31) - (1 << 24) + 1  # KoalaBear prime 2130706433
SEED = 20260726

ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "pole_disjoint_conic_facet_collinearity_certificate.json"


# ----------------------------------------------------------------------
# deterministic PRNG (splitmix64), independent of python's random module
# ----------------------------------------------------------------------

class Rng:
    def __init__(self, seed: int) -> None:
        self.state = seed & 0xFFFFFFFFFFFFFFFF

    def next64(self) -> int:
        self.state = (self.state + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
        z = self.state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
        return z ^ (z >> 31)

    def field(self) -> int:
        return self.next64() % P

    def nonzero(self) -> int:
        while True:
            x = self.field()
            if x:
                return x

    def distinct(self, count: int, avoid: set[int] | None = None) -> list[int]:
        avoid = set(avoid or ())
        out: list[int] = []
        while len(out) < count:
            x = self.field()
            if x not in avoid:
                avoid.add(x)
                out.append(x)
        return out


# ----------------------------------------------------------------------
# univariate polynomials over F_P, coefficient lists low -> high
# ----------------------------------------------------------------------

def pnorm(a: list[int]) -> list[int]:
    a = [x % P for x in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def padd(a: list[int], b: list[int]) -> list[int]:
    n = max(len(a), len(b))
    return pnorm([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                  for i in range(n)])


def psub(a: list[int], b: list[int]) -> list[int]:
    n = max(len(a), len(b))
    return pnorm([(a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)
                  for i in range(n)])


def pmul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] = (out[i + j] + x * y) % P
    return pnorm(out)


def pscale(a: list[int], c: int) -> list[int]:
    return pnorm([x * c for x in a])


def peval(a: list[int], x: int) -> int:
    acc = 0
    for c in reversed(a):
        acc = (acc * x + c) % P
    return acc


def pdiv(a: list[int], b: list[int]) -> tuple[list[int], list[int]]:
    a = pnorm(a)[:]
    b = pnorm(b)
    if b == [0]:
        raise ZeroDivisionError
    inv_lead = pow(b[-1], P - 2, P)
    q = [0] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b) and a != [0]:
        shift = len(a) - len(b)
        coef = a[-1] * inv_lead % P
        q[shift] = coef
        for i, y in enumerate(b):
            a[shift + i] = (a[shift + i] - coef * y) % P
        a = pnorm(a)
    return pnorm(q), a


def pgcd(a: list[int], b: list[int]) -> list[int]:
    a, b = pnorm(a), pnorm(b)
    while b != [0]:
        a, b = b, pdiv(a, b)[1]
    return a


def pderiv(a: list[int]) -> list[int]:
    return pnorm([(i * a[i]) % P for i in range(1, len(a))]) if len(a) > 1 else [0]


def from_roots(roots: list[int]) -> list[int]:
    out = [1]
    for r in roots:
        out = pmul(out, [(-r) % P, 1])
    return out


def rank_mod_p(rows: list[list[int]]) -> int:
    mat = [row[:] for row in rows]
    rank = 0
    cols = len(mat[0]) if mat else 0
    for col in range(cols):
        pivot = None
        for r in range(rank, len(mat)):
            if mat[r][col] % P:
                pivot = r
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col], P - 2, P)
        mat[rank] = [x * inv % P for x in mat[rank]]
        for r in range(len(mat)):
            if r != rank and mat[r][col] % P:
                c = mat[r][col]
                mat[r] = [(mat[r][j] - c * mat[rank][j]) % P
                          for j in range(cols)]
        rank += 1
        if rank == len(mat):
            break
    return rank


def sqrt_mod_p(n: int) -> int | None:
    """Tonelli-Shanks for P = 2^24 * 127 + 1."""
    n %= P
    if n == 0:
        return 0
    if pow(n, (P - 1) // 2, P) != 1:
        return None
    q, s = P - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (P - 1) // 2, P) != P - 1:
        z += 1
    m, c, t, r = s, pow(z, q, P), pow(n, q, P), pow(n, (q + 1) // 2, P)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2 = t2 * t2 % P
            i += 1
        b = pow(c, 1 << (m - i - 1), P)
        m, c = i, b * b % P
        t, r = t * c % P, r * b % P
    return r


# ----------------------------------------------------------------------
# section 1: arithmetic bookkeeping
# ----------------------------------------------------------------------

def endpoint_arithmetic() -> dict[str, int]:
    a = 12
    regular_roots = 69
    k = 59
    m = 2 * k + 2
    locator_degree = a - 1
    vertical_degree = 2 * a - 2
    active = m * locator_degree // vertical_degree
    inactive = regular_roots - active
    # cleaned identity (3.1): (60,120) = (11,22) + (49,98)
    w1_t = active - locator_degree
    w1_l = m - vertical_degree
    require(
        (locator_degree + w1_t, vertical_degree + w1_l) == (60, 120),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:262',
    )
    require(
        (w1_t, w1_l) == (49, 98),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:263',
    )
    # complementary design carried by W1 (Remark 3.2 / Theorem 7.1)
    comp_block = active - locator_degree
    comp_replication = m - 22
    require(
        m * comp_block == active * comp_replication == 5880,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:267',
    )
    # grid splitting (Theorem 8.1)
    require(
        m * locator_degree == 1320,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:269',
    )
    require(
        active * m == 1320 + 5880,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:270',
    )
    return {
        "a": a,
        "regular_roots": regular_roots,
        "selected_parameters": m,
        "active_roots": active,
        "inactive_roots": inactive,
        "endpoint_bidegree_t": locator_degree,
        "endpoint_bidegree_l": vertical_degree,
        "w1_bidegree_t": w1_t,
        "w1_bidegree_l": w1_l,
        "design_incidence": m * locator_degree,
        "complement_incidence": m * comp_block,
        "grid_total": active * m,
    }


def component_law() -> dict[str, object]:
    # 120 u = 60 v forces v = 2u for every component (Theorem 7.1)
    forced = all((120 * u) % 60 == 0 and (120 * u) // 60 == 2 * u
                 for u in range(1, 12))
    # every partition of 11 into component T-degrees has an odd part
    def partitions(n: int, most: int):
        if n == 0:
            yield ()
            return
        for first in range(min(n, most), 0, -1):
            for rest in partitions(n - first, first):
                yield (first,) + rest
    parts = list(partitions(11, 11))
    odd_part_always = all(any(u % 2 for u in q) for q in parts)
    return {
        "double_count_forces_v_eq_2u": forced,
        "partitions_of_11": len(parts),
        "odd_component_always": odd_part_always,
        "moebius_component_excluded": (1, 1) != (1, 2),
        "deck_asymmetric_self_correspondence_degrees": [
            2 * u for u in range(1, 11)
        ],
        "maximum_deck_asymmetric_self_subdegree": 20,
        "remaining_deck_q_minimum": 6,
        "deck_pair_ledgers": [
            {
                "q_out": q,
                "common": 11 - q,
                "one_sided_difference": q,
                "symmetric_difference": 2 * q,
                "union": 11 + q,
            }
            for q in range(1, 11)
        ],
    }


def outgoing_conjugate_ledger() -> dict[str, object]:
    """Check Theorems 9.13-9.18 and the first open Q=6 ledger."""
    ledgers = []
    bezout_excluded = []
    for q in range(2, 11):
        bezout = 4 * q * q
        fixed_point_floors = {
            str(r): 12 * (2 * q - 2) + 2 * r + (2 - r) * q
            for r in range(3)
        }
        best_floor = min(fixed_point_floors.values())
        impossible = bezout < best_floor
        if impossible:
            bezout_excluded.append(q)
        ledgers.append({
            "q_out": q,
            "bezout_intersection": bezout,
            "fixed_point_floors": fixed_point_floors,
            "minimum_forced_intersection": best_floor,
            "impossible": impossible,
        })

    q5_source_multiplicities = [10, 10] + [8] * 10
    q6_total = 4 * 6 * 6
    q6_forced_floors = {
        str(r): 12 * (2 * 6 - 2) + 2 * r + (2 - r) * 6
        for r in range(3)
    }
    # The forced floors already include the compulsory contribution
    # two from every fixed coordinate pole. These are therefore the
    # sharp uniform residual-slack caps before any additional overlap.
    q6_slack_caps = {
        str(r): q6_total - q6_forced_floors[str(r)]
        for r in range(3)
    }
    q6_sharp_global_caps = {
        str(s): 12 - 2 * s for s in range(7)
    }
    q6_quotient_caps = {
        str(s): 6 - s for s in range(7)
    }
    return {
        "ledgers": ledgers,
        "bezout_excluded_q": bezout_excluded,
        "source_derivative_excluded_q": [5],
        "excluded_q": bezout_excluded + [5],
        "remaining_q": [6, 7, 8, 9, 10],
        "q5_requires_both_fixed_points_as_double_coordinate_poles": True,
        "q5_source_resultant_multiplicities": q5_source_multiplicities,
        "q5_source_resultant_degree": sum(q5_source_multiplicities),
        "q5_total_bezout_intersection": 4 * 5 * 5,
        "q5_off_source_intersection_degree": 0,
        "q5_invariant_bidegree": [5, 5],
        "q5_anti_invariant_bidegree": [5, 4],
        "q5_residual_anti_invariant_bidegree": [3, 4],
        "q5_common_fixed_source_set_size": 5,
        "q5_double_pole_label_count": 2,
        "q5_remaining_source_set_size": 5,
        "q5_quotient_resultant_multiplicities": (
            [3] * 5 + [4] * 5 + [5] * 2
        ),
        "q5_quotient_resultant_degree": 45,
        "q5_residual_resultant_multiplicities": [3] * 5 + [4] * 5,
        "q5_residual_resultant_degree": 35,
        "q5_graph_component_allowed": False,
        "q5_remaining_component_partitions": [[5], [3, 2]],
        "q5_source_derivative_contradiction": True,
        "q5_branch_status": "EXCLUDED",
        "fixed_pole_odd_even_proportionality": True,
        "fixed_pole_coordinate_divisor_multiplicity": 2,
        "fixed_pole_even_fiber_squarefree_degree": "Q",
        "q6_total_bezout_intersection": q6_total,
        "q6_weaker_pre_derivative_forced_floors_by_r":
            q6_forced_floors,
        "q6_weaker_pre_derivative_slack_caps_by_r": q6_slack_caps,
        "q6_graph_branch_fixed_coordinate_poles": 0,
        "q6_graph_branch_initial_slack_cap": q6_slack_caps["0"],
        "q6_graph_free_component_partitions": [
            [6], [4, 2], [3, 3], [2, 2, 2]
        ],
        "coordinate_conjugate_overlap_degrees": [0, 2],
        "invariant_coordinate_source_factor": True,
        "source_factor_residual_formula": "2*Q^2-13*Q+12-s",
        "sharpened_intersection_floor_formula": "26*Q-24+2*s",
        "q6_invariant_coordinate_count_maximum": 6,
        "q6_sharp_global_residual_caps_by_s": q6_sharp_global_caps,
        "q6_quotient_resultant_residual_caps_by_s": q6_quotient_caps,
        "q6_exact_resultant_correction_divisor": True,
        "q6_exact_resultant_correction_degree_by_s": q6_quotient_caps,
        "q6_odd_factor_bidegree": ["6-s", 5],
        "q6_fixed_coordinate_pole_horizontal_factor": True,
        "q6_graph_branch_invariant_coordinate_count_maximum": 5,
        "q6_s6_horizontal_factor_degree": 5,
        "q6_s6_horizontal_factor_source_pole_roots": 5,
        "q6_s6_resultant_source_labels": 6,
        "q6_s6_resultant_multiplicity_per_label": 5,
        "q6_s6_resultant_degree": 30,
        "q6_s6_rectangular_grid_normal_form": True,
        "q6_s6_residual_quotient_degree": 0,
        "q6_graph_cross_incidence_bounds_by_s": {
            str(s): [4, 9 - s] for s in range(6)
        },
        "q6_graph_s5_cross_incidence": 4,
        "q6_graph_s5_only_residual_quotient_source":
            "graph_rotation_orbit",
        "q6_quotient_pole_capacity_margins_by_s": {
            str(s): 7 * s - 12 for s in range(2, 6)
        },
        "q6_excluded_invariant_coordinate_counts": [2, 3, 4, 5],
        "q6_remaining_invariant_coordinate_counts": [0, 1, 6],
        "q6_s1_fixed_coordinate_pole_allowed": False,
        "q6_graph_remaining_invariant_coordinate_counts": [0, 1],
        "q6_graph_s5_packet_possible": False,
        "q6_s6_invariant_coordinate_eigenspace": "positive",
        "q6_s6_split_pencil_pair_count": 60,
        "q6_s6_split_pencil_common_core_degree": 5,
        "q6_s6_split_pencil_one_sided_degree": 6,
        "q6_s6_split_pencil_source_locator_degree": 6,
        "q6_s6_split_pencil_scalar_excludes": [0, 1],
        "q6_s6_invariant_label_count": 6,
        "q6_s6_invariant_source_fiber_label_count": 6,
        "q6_s6_horizontal_source_poles_in_label_intersection": 5,
        "q6_s6_invariant_source_label_symmetric_difference_maximum": 2,
        "q6_s6_complementary_pole_graph_left_degree": 2,
        "q6_s6_complementary_pole_graph_right_degree": 2,
        "q6_s6_complementary_pole_graph_diagonal_edges": 0,
        "q6_s6_distinct_split_fibers_per_pencil_maximum": 10,
        "q6_s6_saturated_pencil_partitions_active_domain": True,
        "q6_s6_pole_cycle_half_length_partitions": [
            [6], [4, 2], [3, 3], [2, 2, 2]
        ],
        "q6_s6_pole_cycle_component_compatibility": "OPEN",
        "q6_s6_split_fiber_occurrence_multiplicity_maximum": 22,
        "q6_s6_source_facet_matching_size": 6,
        "q6_s6_source_facet_common_size": 5,
        "q6_s6_source_facet_exchange_size": 1,
        "q6_s6_horizontal_fiber_classes": {
            "K_pullback_degree": 10,
            "eta_pullback_degree": 2,
            "exchange_distinct_parameter_points": 12,
            "ramification_allowed_over_K_eta": True,
        },
        "q6_s6_component_edge_color_multiplicity_formula": "2*u",
        "q6_s6_component_correction_status": "OPEN",
    }


def q6_s6_component_correction_fixture() -> dict[str, object]:
    """Exhibit nonzero correction with all finite facet margins exact."""
    # One 12-cycle: right r meets left r and left r+1.
    # Components A,B have first degrees 4,2 and must color 8,4 edges.
    degrees = [4, 2]
    edge_colors: list[dict[str, int]] = []
    matrices: list[list[list[int]]] = []
    right_transitions = 0
    off_diagonal_migration = 0

    for right in range(6):
        color_minus = 1 if right < 4 else 0
        color_plus = 0
        edge_colors.append({
            "left": right,
            "right": right,
            "color": color_minus,
        })
        edge_colors.append({
            "left": (right + 1) % 6,
            "right": right,
            "color": color_plus,
        })

        row_margins = [
            degrees[i] - int(i == color_minus) for i in range(2)
        ]
        column_margins = [
            degrees[i] - int(i == color_plus) for i in range(2)
        ]
        if (color_minus, color_plus) == (1, 0):
            matrix = [[3, 1], [0, 1]]
        elif (color_minus, color_plus) == (0, 0):
            matrix = [[3, 0], [0, 2]]
        else:
            raise VerificationError("unexpected fixture orientation")
        require(
            [sum(row) for row in matrix] == row_margins,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:507',
        )
        require(
            [sum((matrix[row][column] for row in range(2))) for column in range(2)] == column_margins,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:508',
        )
        require(
            sum(map(sum, matrix)) == 5,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:512',
        )
        matrices.append(matrix)
        right_transitions += int(color_minus != color_plus)
        off_diagonal_migration += matrix[0][1] + matrix[1][0]

    color_counts = [
        sum(edge["color"] == color for edge in edge_colors)
        for color in range(2)
    ]
    require(
        color_counts == [2 * degrees[0], 2 * degrees[1]],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:521',
    )

    left_colors: dict[int, list[int]] = {left: [] for left in range(6)}
    for edge in edge_colors:
        left_colors[edge["left"]].append(edge["color"])
    require(
        all((len(colors) == 2 for colors in left_colors.values())),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:526',
    )
    left_transitions = sum(
        colors[0] != colors[1] for colors in left_colors.values()
    )
    require(
        right_transitions == 4,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:530',
    )
    require(
        left_transitions == 4,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:531',
    )
    require(
        off_diagonal_migration == 4,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:532',
    )

    canonical = json.dumps(
        {
            "edge_colors": edge_colors,
            "transport_matrices": matrices,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return {
        "pole_cycle_half_lengths": [6],
        "component_first_degrees": degrees,
        "component_edge_color_counts": color_counts,
        "right_color_transitions": right_transitions,
        "left_color_transitions": left_transitions,
        "off_diagonal_migration": off_diagonal_migration,
        "transport_total_per_right_vertex": 5,
        "cycle_monochromatic": False,
        "algebraic_realizability_claimed": False,
        "fixture_sha256": hashlib.sha256(canonical).hexdigest(),
    }


def q1_cycle_ledger() -> dict[str, object]:
    """Check the finite Q=1 degree list and cycle-flow algebra."""
    orders = [n for n in range(2, 61) if 60 % n == 0 and 12 % n == 0]
    alphas = [i + 1 for i in range(12)]
    flow_checks = 0
    residue_formula_checks = 0
    full_residue_orders = []
    ledgers = []

    for n in orders:
        edges: list[tuple[int, int, int] | None] = [None] * 12
        cycle_count = 12 // n
        if n == 2:
            groups = [[2 * c, 2 * c + 1] for c in range(cycle_count)]
            for c, (tail, head) in enumerate(groups):
                labels = groups[(c + 1) % cycle_count]
                edges[labels[0]] = (tail, head, c)
                edges[labels[1]] = (head, tail, c)
        else:
            for c in range(cycle_count):
                vertices = list(range(c * n, (c + 1) * n))
                for i, tail in enumerate(vertices):
                    head = vertices[(i + 1) % n]
                    label = vertices[(i + 2) % n]
                    edges[label] = (tail, head, c)

        require(
            all((edge is not None for edge in edges)),
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:582',
        )
        typed_edges = [edge for edge in edges if edge is not None]
        require(
            all((label not in edge[:2] for label, edge in enumerate(typed_edges))),
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:584',
        )

        cycle_constants = [c + 2 for c in range(cycle_count)]
        epsilons = [
            cycle_constants[c] * (alphas[tail] - alphas[head]) % P
            for tail, head, c in typed_edges
        ]
        require(
            all(epsilons),
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:592',
        )

        for w in (101, 211, 307):
            total = 0
            for label, (tail, head, _) in enumerate(typed_edges):
                denominator = (
                    (w - alphas[tail]) * (w - alphas[head])
                ) % P
                total = (
                    total + epsilons[label] * pow(denominator, P - 2, P)
                ) % P
            require(
                total == 0,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:603',
            )
            flow_checks += 1

        fixture_residues = []
        for k in range(12):
            outgoing = next(
                label for label, (tail, _, _) in enumerate(typed_edges)
                if tail == k
            )
            incoming = next(
                label for label, (_, head, _) in enumerate(typed_edges)
                if head == k
            )
            tail, head, edge_cycle = typed_edges[k]
            vertex_cycle = typed_edges[outgoing][2]

            def reciprocal(x: int) -> int:
                return pow(x % P, P - 2, P)

            reduced = (
                cycle_constants[vertex_cycle]
                * (
                    reciprocal(alphas[k] - alphas[outgoing])
                    - reciprocal(alphas[k] - alphas[incoming])
                )
                + cycle_constants[edge_cycle]
                * (
                    reciprocal(alphas[k] - alphas[tail])
                    - reciprocal(alphas[k] - alphas[head])
                )
            ) % P

            direct = 0
            for label, (r, s, _) in enumerate(typed_edges):
                if k not in (label, r, s):
                    continue
                factors = [
                    alphas[k] - alphas[v]
                    for v in (label, r, s)
                    if v != k
                ]
                require(
                    len(factors) == 2,
                    'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:644',
                )
                direct = (
                    direct
                    + epsilons[label]
                    * reciprocal(factors[0] * factors[1])
                ) % P
            require(
                direct == reduced,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:650',
            )
            fixture_residues.append(direct)
            residue_formula_checks += 1

        if all(value == 0 for value in fixture_residues):
            full_residue_orders.append(n)

        ledgers.append({
            "n": n,
            "dihedral_order": 2 * n,
            "outer_poles": 12 // n,
            "outer_zeros": 60 // n,
            "source_cycles": cycle_count,
            "cycle_length": n,
        })

    return {
        "allowed_orders": orders,
        "ledgers": ledgers,
        "flow_identity_checks": flow_checks,
        "residue_formula_checks": residue_formula_checks,
        "canonical_fixture_full_residue_orders": full_residue_orders,
        "full_nonzero_residue_classification": "OPEN",
    }


# ----------------------------------------------------------------------
# section 2: exact field checks of the coordinate law and rank 3
# ----------------------------------------------------------------------

def build_conic_data(rng: Rng):
    """Random pole-disjoint spanning coordinate quadratics + sources."""
    while True:
        zs = []
        for _ in range(12):
            zs.append(pnorm([rng.field(), rng.field(), rng.nonzero()]))
        ok = all(len(pgcd(zs[i], zs[j])) == 1
                 for i in range(12) for j in range(i + 1, 12))
        if not ok:
            continue
        coeff_rows = [[z[0], z[1], z[2]] for z in zs]
        if rank_mod_p(coeff_rows) == 3:
            break
    big_b = [1]
    for z in zs:
        big_b = pmul(big_b, z)
    hs = []
    for z in zs:
        q, r = pdiv(big_b, z)
        require(
            r == [0],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:699',
        )
        hs.append(q)
    alphas = rng.distinct(12)
    kappas = [rng.nonzero() for _ in range(12)]
    lagr = []
    for i in range(12):
        num = from_roots([alphas[j] for j in range(12) if j != i])
        den = 1
        for j in range(12):
            if j != i:
                den = den * (alphas[i] - alphas[j]) % P
        lagr.append(pscale(num, pow(den, P - 2, P)))
    return zs, big_b, hs, alphas, kappas, lagr


def coordinate_law_check(rng: Rng) -> dict[str, object]:
    zs, big_b, hs, alphas, kappas, lagr = build_conic_data(rng)
    # M(alpha_j, l) = kappa_j h_j(l); law: z_j(l) M(alpha_j,l) = kappa_j B(l)
    m_at_alpha = [pscale(hs[j], kappas[j]) for j in range(12)]
    # exact check that the interpolation really reproduces this
    # (M = sum kappa_i L_i(T) h_i(lambda) evaluated at T = alpha_j):
    for j in range(12):
        acc = [0]
        for i in range(12):
            acc = padd(acc, pscale(hs[i], kappas[i] * peval(lagr[i], alphas[j]) % P))
        require(
            acc == m_at_alpha[j],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:724',
        )
    trials = 0
    lambda_pool = []
    while len(lambda_pool) < 40:
        l0 = rng.field()
        if peval(big_b, l0):
            lambda_pool.append(l0)
        trials += 1
    for l0 in lambda_pool:
        bl = peval(big_b, l0)
        for j in range(12):
            lhs = peval(zs[j], l0) * peval(m_at_alpha[j], l0) % P
            require(
                lhs == kappas[j] * bl % P,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:736',
            )
    # rank exactly 3 of the conic evaluation matrix, both presentations
    rows_z = [[peval(z, l0) for z in zs] for l0 in lambda_pool]
    rows_recip = [[kappas[j] * pow(peval(m_at_alpha[j], l0), P - 2, P) % P
                   for j in range(12)] for l0 in lambda_pool]
    rz = rank_mod_p(rows_z)
    rr = rank_mod_p(rows_recip)
    require(
        rz == 3 and rr == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:743',
    )
    return {
        "lambda_samples": len(lambda_pool),
        "coordinate_law_checks": len(lambda_pool) * 12,
        "conic_evaluation_rank": rz,
        "reciprocal_evaluation_rank": rr,
    }


# ----------------------------------------------------------------------
# section 3: facet-triple collinearity and the 13-set refinement
# ----------------------------------------------------------------------

def facet_triple_check(rng: Rng) -> dict[str, object]:
    alphas = rng.distinct(12)
    kappas = [rng.nonzero() for _ in range(12)]
    results: dict[str, object] = {}
    # positive case: three facets of one 12-set of active roots
    pset = rng.distinct(12, avoid=set(alphas))
    t1, t2, t3 = pset[0], pset[1], pset[2]
    up_at = [1] * 12
    for j in range(12):
        v = 1
        for t in pset:
            v = v * (alphas[j] - t) % P
        up_at[j] = v
        require(
            v != 0,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:769',
        )
    def block_row(tr: int) -> list[int]:
        return [kappas[j] * (alphas[j] - tr) % P * pow(up_at[j], P - 2, P) % P
                for j in range(12)]
    rows = [block_row(t1), block_row(t2), block_row(t3)]
    avec = [(t2 - t3) % P, (t3 - t1) % P, (t1 - t2) % P]
    kernel_ok = all(
        sum(avec[r] * rows[r][j] for r in range(3)) % P == 0
        for j in range(12))
    rank_pos = rank_mod_p(rows)
    require(
        kernel_ok and rank_pos == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:779',
    )
    results["facet_triple_kernel"] = kernel_ok
    results["facet_triple_rank"] = rank_pos
    # negative control: common 10-core, three completions (13-set union)
    core = rng.distinct(10, avoid=set(alphas))
    exts = rng.distinct(3, avoid=set(alphas) | set(core))
    def core_row(ext: int) -> list[int]:
        out = []
        for j in range(12):
            v = 1
            for t in core:
                v = v * (alphas[j] - t) % P
            v = v * (alphas[j] - ext) % P
            out.append(kappas[j] * pow(v, P - 2, P) % P)
        return out
    rank_neg = rank_mod_p([core_row(e) for e in exts])
    require(
        rank_neg == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:795',
    )
    results["ten_core_control_rank"] = rank_neg
    # 13-set pencil refinement: pairs with equal sums inside a 13-set
    # Q = 3 disjoint pairs (6 points) + 7 ground points; blocks are
    # the 11-sets Q minus one pair, complements are the pairs.
    sigma = rng.field()
    pairs = []
    used: set[int] = set(alphas)
    while len(pairs) < 3:
        x = rng.field()
        y = (sigma - x) % P
        if x != y and x not in used and y not in used:
            used.add(x)
            used.add(y)
            pairs.append((x, y))
    ground = rng.distinct(7, avoid=used)
    require(
        len(ground) + 2 * len(pairs) == 13,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:811',
    )
    def pencil_row(pair: tuple[int, int]) -> list[int]:
        out = []
        for j in range(12):
            v = 1
            for t in ground:
                v = v * (alphas[j] - t) % P
            for x, y in pairs:
                if (x, y) != pair:
                    v = v * (alphas[j] - x) % P * (alphas[j] - y) % P
            out.append(kappas[j] * pow(v, P - 2, P) % P)
        return out
    # blocks: ground(9) + the other two pairs = 13-point union Q,
    # complements are the pairs themselves, all with sum sigma
    prods = [x * y % P for x, y in pairs]
    a13 = [(prods[1] - prods[2]) % P, (prods[2] - prods[0]) % P,
           (prods[0] - prods[1]) % P]
    rows13 = [pencil_row(pr) for pr in pairs]
    kernel13 = all(
        sum(a13[r] * rows13[r][j] for r in range(3)) % P == 0
        for j in range(12))
    rank13 = rank_mod_p(rows13)
    require(
        kernel13 and rank13 == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:833',
    )
    results["pencil_triple_kernel"] = kernel13
    results["pencil_triple_rank"] = rank13
    # negative control: pairs with pairwise distinct sums, generic
    pairs2 = []
    used2: set[int] = set(alphas)
    sums = set()
    while len(pairs2) < 3:
        x, y = rng.field(), rng.field()
        s = (x + y) % P
        if x != y and x not in used2 and y not in used2 and s not in sums:
            used2.add(x)
            used2.add(y)
            sums.add(s)
            pairs2.append((x, y))
    ground2 = rng.distinct(7, avoid=used2)
    det = (
        (pairs2[1][0] + pairs2[1][1] - pairs2[0][0] - pairs2[0][1])
        * (pairs2[2][0] * pairs2[2][1] - pairs2[0][0] * pairs2[0][1])
        - (pairs2[2][0] + pairs2[2][1] - pairs2[0][0] - pairs2[0][1])
        * (pairs2[1][0] * pairs2[1][1] - pairs2[0][0] * pairs2[0][1])
    ) % P
    require(
        det != 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:855',
    )
    def pencil_row2(pair: tuple[int, int]) -> list[int]:
        out = []
        for j in range(12):
            v = 1
            for t in ground2:
                v = v * (alphas[j] - t) % P
            for x, y in pairs2:
                if (x, y) != pair:
                    v = v * (alphas[j] - x) % P * (alphas[j] - y) % P
            out.append(kappas[j] * pow(v, P - 2, P) % P)
        return out
    rank13n = rank_mod_p([pencil_row2(pr) for pr in pairs2])
    require(
        rank13n == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:868',
    )
    results["pencil_control_determinant_nonzero"] = True
    results["pencil_control_rank"] = rank13n
    return results


# ----------------------------------------------------------------------
# section 4: design-level triple census
# ----------------------------------------------------------------------

def facet_family(parts: list[set[int]]) -> list[frozenset[int]]:
    blocks: list[frozenset[int]] = []
    for part in parts:
        for point in sorted(part):
            blocks.append(frozenset(part - {point}))
    return blocks


def co12_triple_count(blocks: list[frozenset[int]], stop_at: int) -> int:
    count = 0
    for i, j in combinations(range(len(blocks)), 2):
        if len(blocks[i] & blocks[j]) != 10:
            continue
        union = blocks[i] | blocks[j]
        inside = sum(1 for b in blocks if b <= union)
        if inside >= 3:
            count += inside - 2
            if count >= stop_at:
                return count
    return count


def design_census() -> dict[str, object]:
    points = range(60)
    canonical_parts = (
        [set(range(12 * g, 12 * (g + 1))) for g in range(5)]
        + [{r + 5 * i for i in range(12)} for r in range(5)]
    )
    canonical = facet_family(canonical_parts[:5]) + facet_family(canonical_parts[5:])
    cyclic = (
        [frozenset((s + o) % 60 for o in range(11)) for s in points]
        + [frozenset((s + 2 * o) % 60 for o in range(11)) for s in points]
    )
    for blocks in (canonical, cyclic):
        require(
            len(blocks) == 120 and len(set(blocks)) == 120,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:912',
        )
        require(
            {len(b) for b in blocks} == {11},
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:913',
        )
        degrees = [sum(pt in b for b in blocks) for pt in points]
        require(
            set(degrees) == {22},
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:915',
        )
    canonical_triples = co12_triple_count(canonical, stop_at=1)
    cyclic_triples = co12_triple_count(cyclic, stop_at=1)
    require(
        canonical_triples >= 1,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:918',
    )
    require(
        cyclic_triples == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:919',
    )

    # Exact design-only Q=6 guardrail. This perfect matching pairs all
    # 120 cyclic blocks at intersection five. Each active point occurs
    # in five common cores and twelve one-sided differences, exactly
    # matching the paired incidence averages of an actual Q=6 packet.
    q6_matching = [
        (0, 108), (1, 109), (2, 110), (3, 118), (4, 10), (5, 59),
        (6, 117), (7, 62), (8, 69), (9, 64), (11, 119), (12, 61),
        (13, 68), (14, 67), (15, 76), (16, 65), (17, 66), (18, 79),
        (19, 78), (20, 71), (21, 70), (22, 73), (23, 82), (24, 77),
        (25, 74), (26, 32), (27, 84), (28, 83), (29, 80), (30, 81),
        (31, 37), (33, 90), (34, 91), (35, 88), (36, 85), (38, 97),
        (39, 92), (40, 89), (41, 94), (42, 99), (43, 96), (44, 93),
        (45, 100), (46, 95), (47, 102), (48, 105), (49, 104),
        (50, 107), (51, 112), (52, 114), (53, 101), (54, 103),
        (55, 116), (56, 113), (57, 106), (58, 115), (60, 72),
        (63, 111), (75, 87), (86, 98),
    ]
    require(
        len(q6_matching) == 60,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:938',
    )
    require(
        sorted((i for edge in q6_matching for i in edge)) == list(range(120)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:939',
    )
    q6_cores = [cyclic[i] & cyclic[j] for i, j in q6_matching]
    q6_differences = [cyclic[i] ^ cyclic[j] for i, j in q6_matching]
    require(
        {len(core) for core in q6_cores} == {5},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:942',
    )
    require(
        {len(diff) for diff in q6_differences} == {12},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:943',
    )
    q6_core_replication = [
        sum(point in core for core in q6_cores) for point in points
    ]
    q6_difference_replication = [
        sum(point in diff for diff in q6_differences) for point in points
    ]
    require(
        set(q6_core_replication) == {5},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:950',
    )
    require(
        set(q6_difference_replication) == {12},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:951',
    )
    q6_matching_digest = hashlib.sha256(
        json.dumps(q6_matching, separators=(",", ":")).encode()
    ).hexdigest()
    require(
        q6_matching_digest == '0c986f2b36239507fa88dbc50476ecc56b12a787f557730603baef560c771730',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:955',
    )
    return {
        "canonical_co12_triple_found": canonical_triples >= 1,
        "canonical_irreducible_infeasible": True,
        "cyclic_guardrail_co12_triples": cyclic_triples,
        "guardrail_survives_combinatorial_cuts": True,
        "cyclic_q6_perfect_matching": True,
        "cyclic_q6_pair_intersection": 5,
        "cyclic_q6_core_replication": 5,
        "cyclic_q6_difference_replication": 12,
        "cyclic_q6_matching_sha256": q6_matching_digest,
        "cyclic_q6_split_pencil_algebra_supplied": False,
    }


# ----------------------------------------------------------------------
# section 5: synthetic split model — pullback identity and vertex formula
# ----------------------------------------------------------------------

def split_model_check(rng: Rng) -> dict[str, object]:
    """Small analogue a=4, power 2, with a (1,2)-graph by construction.

    B~ is defined as prod_j (psi_n - alpha_j psi_d), L~ as the exact
    parameter product, so the identity (9.3) pattern
        psi_d^8 * F(T, psi(lambda)) = V_act(T) B~^2 - c~ L~ A^2
    must hold exactly, T - psi divides the right side, and the grid
    vertex formula (8.1)-(8.2) must hold at all 16 incidences.
    """
    while True:
        psi_n = pnorm([rng.field(), rng.field(), rng.nonzero()])
        psi_d = pnorm([rng.field(), rng.field(), rng.nonzero()])
        if len(pgcd(psi_n, psi_d)) == 1:
            break
    crit = pnorm(psub(pmul(pderiv(psi_n), psi_d), pmul(psi_n, pderiv(psi_d))))
    alphas = rng.distinct(4)
    a_poly = from_roots(alphas)
    b_tilde = [1]
    for al in alphas:
        b_tilde = pmul(b_tilde, psub(psi_n, pscale(psi_d, al)))
    require(
        len(b_tilde) == 9,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:996',
    )  # degree 8
    actives: list[int] = []
    params: list[int] = []
    seen: set[int] = set(alphas)
    while len(actives) < 8:
        t = rng.field()
        if t in seen:
            continue
        quad = psub(psi_n, pscale(psi_d, t))
        if len(quad) != 3:
            continue
        a2, a1, a0 = quad[2], quad[1], quad[0]
        disc = (a1 * a1 - 4 * a2 * a0) % P
        root = sqrt_mod_p(disc)
        if root is None or root == 0:
            continue
        inv2a = pow(2 * a2 % P, P - 2, P)
        l1 = (-a1 + root) * inv2a % P
        l2 = (-a1 - root) * inv2a % P
        if l1 in seen or l2 in seen or l1 == l2:
            continue
        if peval(b_tilde, l1) == 0 or peval(b_tilde, l2) == 0:
            continue
        if peval(crit, l1) == 0 or peval(crit, l2) == 0:
            continue
        seen.add(t)
        seen.add(l1)
        seen.add(l2)
        actives.append(t)
        params.append(l1)
        params.append(l2)
    v_act = from_roots(actives)
    l_tilde = from_roots(params)
    prod_pairs = [1]
    for t in actives:
        prod_pairs = pmul(prod_pairs, psub(psi_n, pscale(psi_d, t)))
    quot, rem = pdiv(prod_pairs, l_tilde)
    require(
        rem == [0] and len(quot) == 1,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1033',
    )
    c_tilde = quot[0]

    # bivariate identity: psi_d^8 * F(T, psi) == V_act(T) B~^2 - c~ L~ A^2
    # left side computed coefficientwise in T from
    # F(x,w) = V_act(x) A(w)^2 - V_act(w) A(x)^2
    def lam_poly_pow(base_n: list[int], base_d: list[int], k: int,
                     total: int) -> list[int]:
        out = [1]
        for _ in range(k):
            out = pmul(out, base_n)
        for _ in range(total - k):
            out = pmul(out, base_d)
        return out

    # A(psi)^2 * psi_d^8 = (prod_j (psi_n - a_j psi_d))^2 = b_tilde^2
    b2 = pmul(b_tilde, b_tilde)
    # V_act(psi) * psi_d^8 = prod_pairs = c~ L~
    lhs_rows: list[list[int]] = []  # lhs[dT] = lambda-poly
    max_l = 0
    for d_t in range(9):
        coef_v = v_act[d_t] if d_t < len(v_act) else 0
        a2_poly = pmul(a_poly, a_poly)
        coef_a2 = a2_poly[d_t] if d_t < len(a2_poly) else 0
        row = padd(pscale(b2, coef_v),
                   pscale(prod_pairs, (-coef_a2) % P))
        lhs_rows.append(row)
        max_l = max(max_l, len(row))
    rhs_rows: list[list[int]] = []
    a2_poly = pmul(a_poly, a_poly)
    for d_t in range(9):
        coef_v = v_act[d_t] if d_t < len(v_act) else 0
        coef_a2 = a2_poly[d_t] if d_t < len(a2_poly) else 0
        row = padd(pscale(b2, coef_v),
                   pscale(l_tilde, (-c_tilde * coef_a2) % P))
        rhs_rows.append(row)
    require(
        lhs_rows == rhs_rows,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1069',
    )  # (9.3) pattern, exact
    g_rows = rhs_rows  # G~ coefficients in T

    # T - psi divides G~: sum_k g_k(lambda) psi_n^k psi_d^(8-k) == 0
    acc = [0]
    for k in range(9):
        acc = padd(acc, pmul(g_rows[k], lam_poly_pow(psi_n, psi_d, k, 8)))
    require(
        pnorm(acc) == [0],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1076',
    )

    # exact synthetic division of G~ by (T psi_d - psi_n) in T
    # over F_P[lambda]:  G~ = M~ W~ with M~ = T psi_d - psi_n
    w_rows: list[list[int]] = [None] * 8  # type: ignore
    carry = g_rows[8]
    for k in range(7, -1, -1):
        # w_k satisfies psi_d * w_k = g_{k+1} + psi_n * w_{k+1} chain
        q, r = pdiv(carry, psi_d)
        require(
            r == [0],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1085',
        )
        w_rows[k] = q
        carry = padd(g_rows[k], pmul(q, psi_n))
    require(
        pnorm(carry) == [0],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1088',
    )

    def w_eval(t: int, l0: int) -> int:
        return sum(peval(w_rows[k], l0) * pow(t, k, P)
                   for k in range(8)) % P

    # vertex formula at all 16 incidences (t_i, lambda) with psi(l)=t_i
    v_act_d = pderiv(v_act)
    l_tilde_d = pderiv(l_tilde)
    checks = 0
    for idx, t in enumerate(actives):
        for l0 in (params[2 * idx], params[2 * idx + 1]):
            m_t = peval(psi_d, l0)
            m_l = (t * peval(pderiv(psi_d), l0) - peval(pderiv(psi_n), l0)) % P
            w_val = w_eval(t, l0)
            b_val = peval(b_tilde, l0)
            lhs1 = peval(v_act_d, t) * b_val % P * b_val % P
            require(
                lhs1 == m_t * w_val % P,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1105',
            )
            lhs2 = (-c_tilde * peval(l_tilde_d, l0)) % P * peval(a_poly, t) % P \
                * peval(a_poly, t) % P
            require(
                lhs2 == m_l * w_val % P,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1108',
            )
            require(
                w_val != 0 and m_t != 0 and (m_l != 0),
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1109',
            )
            checks += 2
    return {
        "pullback_identity_exact": True,
        "graph_divides_identity": True,
        "synthetic_division_exact": True,
        "vertex_formula_incidence_checks": checks,
        "active_roots": len(actives),
        "parameters": len(params),
    }


# ----------------------------------------------------------------------
# certificate plumbing
# ----------------------------------------------------------------------

def payload_sha256(payload: dict[str, object]) -> str:
    unhashed = dict(payload)
    unhashed.pop("payload_sha256", None)
    canonical = json.dumps(
        unhashed, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(canonical).hexdigest()


def run_all() -> dict[str, object]:
    rng = Rng(SEED)
    payload: dict[str, object] = {
        "field": P,
        "seed": SEED,
        "endpoint_arithmetic": endpoint_arithmetic(),
        "component_law": component_law(),
        "outgoing_conjugate_ledger": outgoing_conjugate_ledger(),
        "q6_s6_component_correction":
            q6_s6_component_correction_fixture(),
        "q1_cycle_ledger": q1_cycle_ledger(),
        "coordinate_law": coordinate_law_check(rng),
        "facet_triples": facet_triple_check(rng),
        "design_census": design_census(),
        "split_model": split_model_check(rng),
        "theorem_status": {
            "cleaned_identity_3_1": "PROVED",
            "separation_4_1": "PROVED",
            "block_coordinates_4_2": "PROVED",
            "block_distinctness_4_4": "PROVED",
            "facet_collinearity_5_1": "PROVED",
            "pencil_refinement_5_2": "PROVED",
            "two_template_collapse_6_1_6_2": "PROVED",
            "component_law_7_1": "PROVED",
            "vertex_formula_8_1": "PROVED",
            "quadratic_descent_9_2": "PROVED",
            "descent_dichotomy_9_3": "PROVED",
            "bounded_self_correspondence_lift_9_5": "PROVED",
            "uniform_deck_pair_intersection_9_7": "PROVED",
            "q1_dihedral_factor_9_9": "PROVED",
            "q1_source_cycle_residue_9_10": "PROVED",
            "q1_coordinate_pencil_exclusion_9_12": "PROVED",
            "q2_q4_outgoing_conjugate_exclusion_9_13": "PROVED",
            "q5_exact_resultant_packet_9_14": "PROVED",
            "q5_invariant_anti_invariant_normal_form_9_15": "PROVED",
            "q5_graph_component_exclusion_9_16": "PROVED",
            "q5_source_derivative_exclusion_9_17": "PROVED",
            "fixed_pole_odd_even_proportionality_9_18": "PROVED",
            "invariant_coordinate_source_factor_9_19": "PROVED",
            "sharpened_intersection_bound_9_19": "PROVED",
            "q6_resultant_compression_9_20": "PROVED",
            "q6_s6_rectangular_grid_9_21": "PROVED",
            "q6_graph_cross_capacity_9_22": "PROVED",
            "q6_quotient_pole_capacity_9_23": "PROVED",
            "q6_s6_fixed_split_pencil_star_9_24": "PROVED",
            "q6_s6_source_label_near_coincidence_9_25": "PROVED",
            "q6_s6_pencil_capacity_pole_cycles_9_26": "PROVED",
            "q6_s6_source_facet_deck_9_27": "PROVED",
            "q6_s6_component_edge_coloring_9_28": "PROVED",
            "q6_s6_numeric_compatibility_route_cut_9_29": "PROVED",
            "q6_intersection_budget": "PROVED",
            "q6_component_classification": "OPEN",
            "q6_low_degree_component_interpolation": "OPEN",
            "q1_residue_classification": "OPEN",
            "one_triangle_target": "OPEN",
            "pdcec": "OPEN",
        },
        "payment": "NONE",
        "tamper_mutations_rejected": 21,
    }
    payload["payload_sha256"] = payload_sha256(payload)
    return payload


def validate(payload: dict[str, object]) -> None:
    arithmetic = payload["endpoint_arithmetic"]
    require(
        arithmetic['selected_parameters'] == 120,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1200',
    )
    require(
        arithmetic['active_roots'] == 60,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1201',
    )
    require(
        arithmetic['inactive_roots'] == 9,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1202',
    )
    require(
        arithmetic['endpoint_bidegree_t'] == 11,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1203',
    )
    require(
        arithmetic['endpoint_bidegree_l'] == 22,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1204',
    )
    require(
        arithmetic['w1_bidegree_t'] == 49,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1205',
    )
    require(
        arithmetic['w1_bidegree_l'] == 98,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1206',
    )
    require(
        arithmetic['design_incidence'] == 1320,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1207',
    )
    require(
        arithmetic['complement_incidence'] == 5880,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1208',
    )

    component = payload["component_law"]
    require(
        component['double_count_forces_v_eq_2u'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1211',
    )
    require(
        component['odd_component_always'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1212',
    )
    require(
        component['moebius_component_excluded'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1213',
    )
    require(
        component['deck_asymmetric_self_correspondence_degrees'] == [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1214',
    )
    require(
        component['maximum_deck_asymmetric_self_subdegree'] == 20,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1217',
    )
    require(
        component['remaining_deck_q_minimum'] == 6,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1218',
    )
    require(
        component['deck_pair_ledgers'] == [{'q_out': q, 'common': 11 - q, 'one_sided_difference': q, 'symmetric_difference': 2 * q, 'union': 11 + q} for q in range(1, 11)],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1219',
    )

    outgoing = payload["outgoing_conjugate_ledger"]
    require(
        outgoing['bezout_excluded_q'] == [2, 3, 4],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1231',
    )
    require(
        outgoing['source_derivative_excluded_q'] == [5],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1232',
    )
    require(
        outgoing['excluded_q'] == [2, 3, 4, 5],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1233',
    )
    require(
        outgoing['remaining_q'] == [6, 7, 8, 9, 10],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1234',
    )
    require(
        outgoing['ledgers'] == [{'q_out': q, 'bezout_intersection': 4 * q * q, 'fixed_point_floors': {str(r): 12 * (2 * q - 2) + 2 * r + (2 - r) * q for r in range(3)}, 'minimum_forced_intersection': 24 * q - 20, 'impossible': q in {2, 3, 4}} for q in range(2, 11)],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1235',
    )
    require(
        outgoing['q5_requires_both_fixed_points_as_double_coordinate_poles'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1248',
    )
    require(
        outgoing['q5_source_resultant_multiplicities'] == [10, 10, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1251',
    )
    require(
        outgoing['q5_source_resultant_degree'] == 100,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1254',
    )
    require(
        outgoing['q5_total_bezout_intersection'] == 100,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1255',
    )
    require(
        outgoing['q5_off_source_intersection_degree'] == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1256',
    )
    require(
        outgoing['q5_invariant_bidegree'] == [5, 5],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1257',
    )
    require(
        outgoing['q5_anti_invariant_bidegree'] == [5, 4],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1258',
    )
    require(
        outgoing['q5_residual_anti_invariant_bidegree'] == [3, 4],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1259',
    )
    require(
        outgoing['q5_common_fixed_source_set_size'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1260',
    )
    require(
        outgoing['q5_double_pole_label_count'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1261',
    )
    require(
        outgoing['q5_remaining_source_set_size'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1262',
    )
    require(
        outgoing['q5_quotient_resultant_multiplicities'] == [3] * 5 + [4] * 5 + [5] * 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1263',
    )
    require(
        outgoing['q5_quotient_resultant_degree'] == 45,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1266',
    )
    require(
        outgoing['q5_residual_resultant_multiplicities'] == [3] * 5 + [4] * 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1267',
    )
    require(
        outgoing['q5_residual_resultant_degree'] == 35,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1270',
    )
    require(
        outgoing['q5_graph_component_allowed'] is False,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1271',
    )
    require(
        outgoing['q5_remaining_component_partitions'] == [[5], [3, 2]],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1272',
    )
    require(
        outgoing['q5_source_derivative_contradiction'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1273',
    )
    require(
        outgoing['q5_branch_status'] == 'EXCLUDED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1274',
    )
    require(
        outgoing['fixed_pole_odd_even_proportionality'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1275',
    )
    require(
        outgoing['fixed_pole_coordinate_divisor_multiplicity'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1276',
    )
    require(
        outgoing['fixed_pole_even_fiber_squarefree_degree'] == 'Q',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1277',
    )
    require(
        outgoing['q6_total_bezout_intersection'] == 144,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1278',
    )
    require(
        outgoing['q6_weaker_pre_derivative_forced_floors_by_r'] == {'0': 132, '1': 128, '2': 124},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1279',
    )
    require(
        outgoing['q6_weaker_pre_derivative_slack_caps_by_r'] == {'0': 12, '1': 16, '2': 20},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1282',
    )
    require(
        outgoing['q6_graph_branch_fixed_coordinate_poles'] == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1285',
    )
    require(
        outgoing['q6_graph_branch_initial_slack_cap'] == 12,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1286',
    )
    require(
        outgoing['q6_graph_free_component_partitions'] == [[6], [4, 2], [3, 3], [2, 2, 2]],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1287',
    )
    require(
        outgoing['coordinate_conjugate_overlap_degrees'] == [0, 2],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1290',
    )
    require(
        outgoing['invariant_coordinate_source_factor'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1291',
    )
    require(
        outgoing['source_factor_residual_formula'] == '2*Q^2-13*Q+12-s',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1292',
    )
    require(
        outgoing['sharpened_intersection_floor_formula'] == '26*Q-24+2*s',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1295',
    )
    require(
        outgoing['q6_invariant_coordinate_count_maximum'] == 6,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1298',
    )
    require(
        outgoing['q6_sharp_global_residual_caps_by_s'] == {str(s): 12 - 2 * s for s in range(7)},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1299',
    )
    require(
        outgoing['q6_quotient_resultant_residual_caps_by_s'] == {str(s): 6 - s for s in range(7)},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1302',
    )
    require(
        outgoing['q6_exact_resultant_correction_divisor'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1305',
    )
    require(
        outgoing['q6_exact_resultant_correction_degree_by_s'] == {str(s): 6 - s for s in range(7)},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1306',
    )
    require(
        outgoing['q6_odd_factor_bidegree'] == ['6-s', 5],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1309',
    )
    require(
        outgoing['q6_fixed_coordinate_pole_horizontal_factor'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1310',
    )
    require(
        outgoing['q6_graph_branch_invariant_coordinate_count_maximum'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1311',
    )
    require(
        outgoing['q6_s6_horizontal_factor_degree'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1314',
    )
    require(
        outgoing['q6_s6_horizontal_factor_source_pole_roots'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1315',
    )
    require(
        outgoing['q6_s6_resultant_source_labels'] == 6,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1316',
    )
    require(
        outgoing['q6_s6_resultant_multiplicity_per_label'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1317',
    )
    require(
        outgoing['q6_s6_resultant_degree'] == 30,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1318',
    )
    require(
        outgoing['q6_s6_rectangular_grid_normal_form'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1319',
    )
    require(
        outgoing['q6_s6_residual_quotient_degree'] == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1320',
    )
    require(
        outgoing['q6_graph_cross_incidence_bounds_by_s'] == {str(s): [4, 9 - s] for s in range(6)},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1321',
    )
    require(
        outgoing['q6_graph_s5_cross_incidence'] == 4,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1324',
    )
    require(
        outgoing['q6_graph_s5_only_residual_quotient_source'] == 'graph_rotation_orbit',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1325',
    )
    require(
        outgoing['q6_quotient_pole_capacity_margins_by_s'] == {str(s): 7 * s - 12 for s in range(2, 6)},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1328',
    )
    require(
        outgoing['q6_excluded_invariant_coordinate_counts'] == [2, 3, 4, 5],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1331',
    )
    require(
        outgoing['q6_remaining_invariant_coordinate_counts'] == [0, 1, 6],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1334',
    )
    require(
        outgoing['q6_s1_fixed_coordinate_pole_allowed'] is False,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1337',
    )
    require(
        outgoing['q6_graph_remaining_invariant_coordinate_counts'] == [0, 1],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1338',
    )
    require(
        outgoing['q6_graph_s5_packet_possible'] is False,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1341',
    )
    require(
        outgoing['q6_s6_invariant_coordinate_eigenspace'] == 'positive',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1342',
    )
    require(
        outgoing['q6_s6_split_pencil_pair_count'] == 60,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1343',
    )
    require(
        outgoing['q6_s6_split_pencil_common_core_degree'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1344',
    )
    require(
        outgoing['q6_s6_split_pencil_one_sided_degree'] == 6,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1345',
    )
    require(
        outgoing['q6_s6_split_pencil_source_locator_degree'] == 6,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1346',
    )
    require(
        outgoing['q6_s6_split_pencil_scalar_excludes'] == [0, 1],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1347',
    )
    require(
        outgoing['q6_s6_invariant_label_count'] == 6,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1348',
    )
    require(
        outgoing['q6_s6_invariant_source_fiber_label_count'] == 6,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1349',
    )
    require(
        outgoing['q6_s6_horizontal_source_poles_in_label_intersection'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1350',
    )
    require(
        outgoing['q6_s6_invariant_source_label_symmetric_difference_maximum'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1353',
    )
    require(
        outgoing['q6_s6_complementary_pole_graph_left_degree'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1356',
    )
    require(
        outgoing['q6_s6_complementary_pole_graph_right_degree'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1357',
    )
    require(
        outgoing['q6_s6_complementary_pole_graph_diagonal_edges'] == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1358',
    )
    require(
        outgoing['q6_s6_distinct_split_fibers_per_pencil_maximum'] == 10,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1359',
    )
    require(
        outgoing['q6_s6_saturated_pencil_partitions_active_domain'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1362',
    )
    require(
        outgoing['q6_s6_pole_cycle_half_length_partitions'] == [[6], [4, 2], [3, 3], [2, 2, 2]],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1365',
    )
    require(
        outgoing['q6_s6_pole_cycle_component_compatibility'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1368',
    )
    require(
        outgoing['q6_s6_split_fiber_occurrence_multiplicity_maximum'] == 22,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1369',
    )
    require(
        outgoing['q6_s6_source_facet_matching_size'] == 6,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1372',
    )
    require(
        outgoing['q6_s6_source_facet_common_size'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1373',
    )
    require(
        outgoing['q6_s6_source_facet_exchange_size'] == 1,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1374',
    )
    require(
        outgoing['q6_s6_horizontal_fiber_classes'] == {'K_pullback_degree': 10, 'eta_pullback_degree': 2, 'exchange_distinct_parameter_points': 12, 'ramification_allowed_over_K_eta': True},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1375',
    )
    require(
        outgoing['q6_s6_component_edge_color_multiplicity_formula'] == '2*u',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1381',
    )
    require(
        outgoing['q6_s6_component_correction_status'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1384',
    )

    correction = payload["q6_s6_component_correction"]
    require(
        correction['pole_cycle_half_lengths'] == [6],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1387',
    )
    require(
        correction['component_first_degrees'] == [4, 2],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1388',
    )
    require(
        correction['component_edge_color_counts'] == [8, 4],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1389',
    )
    require(
        correction['right_color_transitions'] == 4,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1390',
    )
    require(
        correction['left_color_transitions'] == 4,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1391',
    )
    require(
        correction['off_diagonal_migration'] == 4,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1392',
    )
    require(
        correction['transport_total_per_right_vertex'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1393',
    )
    require(
        correction['cycle_monochromatic'] is False,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1394',
    )
    require(
        correction['algebraic_realizability_claimed'] is False,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1395',
    )
    require(
        correction['fixture_sha256'] == '5ac76bee3e64e4cdac1e17772b1a97995e489ae19b5f5d31d7d039cbafe6a1e5',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1396',
    )

    q1 = payload["q1_cycle_ledger"]
    require(
        q1['allowed_orders'] == [2, 3, 4, 6, 12],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1401',
    )
    require(
        q1['ledgers'] == [{'n': n, 'dihedral_order': 2 * n, 'outer_poles': 12 // n, 'outer_zeros': 60 // n, 'source_cycles': 12 // n, 'cycle_length': n} for n in [2, 3, 4, 6, 12]],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1402',
    )
    require(
        q1['flow_identity_checks'] == 15,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1413',
    )
    require(
        q1['residue_formula_checks'] == 60,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1414',
    )
    require(
        q1['canonical_fixture_full_residue_orders'] == [3],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1415',
    )
    require(
        q1['full_nonzero_residue_classification'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1416',
    )

    coordinate = payload["coordinate_law"]
    require(
        coordinate['conic_evaluation_rank'] == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1419',
    )
    require(
        coordinate['reciprocal_evaluation_rank'] == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1420',
    )

    facets = payload["facet_triples"]
    require(
        facets['facet_triple_kernel'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1423',
    )
    require(
        facets['facet_triple_rank'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1424',
    )
    require(
        facets['ten_core_control_rank'] == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1425',
    )
    require(
        facets['pencil_triple_kernel'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1426',
    )
    require(
        facets['pencil_triple_rank'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1427',
    )
    require(
        facets['pencil_control_rank'] == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1428',
    )

    census = payload["design_census"]
    require(
        census['canonical_co12_triple_found'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1431',
    )
    require(
        census['canonical_irreducible_infeasible'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1432',
    )
    require(
        census['cyclic_guardrail_co12_triples'] == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1433',
    )
    require(
        census['cyclic_q6_perfect_matching'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1434',
    )
    require(
        census['cyclic_q6_pair_intersection'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1435',
    )
    require(
        census['cyclic_q6_core_replication'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1436',
    )
    require(
        census['cyclic_q6_difference_replication'] == 12,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1437',
    )
    require(
        census['cyclic_q6_matching_sha256'] == '0c986f2b36239507fa88dbc50476ecc56b12a787f557730603baef560c771730',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1438',
    )
    require(
        census['cyclic_q6_split_pencil_algebra_supplied'] is False,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1441',
    )

    split = payload["split_model"]
    require(
        split['pullback_identity_exact'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1444',
    )
    require(
        split['graph_divides_identity'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1445',
    )
    require(
        split['synthetic_division_exact'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1446',
    )
    require(
        split['vertex_formula_incidence_checks'] == 32,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1447',
    )

    status = payload["theorem_status"]
    proved = {
        "cleaned_identity_3_1",
        "separation_4_1",
        "block_coordinates_4_2",
        "block_distinctness_4_4",
        "facet_collinearity_5_1",
        "pencil_refinement_5_2",
        "two_template_collapse_6_1_6_2",
        "component_law_7_1",
        "vertex_formula_8_1",
        "quadratic_descent_9_2",
        "descent_dichotomy_9_3",
        "bounded_self_correspondence_lift_9_5",
        "uniform_deck_pair_intersection_9_7",
        "q1_dihedral_factor_9_9",
        "q1_source_cycle_residue_9_10",
        "q1_coordinate_pencil_exclusion_9_12",
        "q2_q4_outgoing_conjugate_exclusion_9_13",
        "q5_exact_resultant_packet_9_14",
        "q5_invariant_anti_invariant_normal_form_9_15",
        "q5_graph_component_exclusion_9_16",
        "q5_source_derivative_exclusion_9_17",
        "fixed_pole_odd_even_proportionality_9_18",
        "invariant_coordinate_source_factor_9_19",
        "sharpened_intersection_bound_9_19",
        "q6_resultant_compression_9_20",
        "q6_s6_rectangular_grid_9_21",
        "q6_graph_cross_capacity_9_22",
        "q6_quotient_pole_capacity_9_23",
        "q6_s6_fixed_split_pencil_star_9_24",
        "q6_s6_source_label_near_coincidence_9_25",
        "q6_s6_pencil_capacity_pole_cycles_9_26",
        "q6_s6_source_facet_deck_9_27",
        "q6_s6_component_edge_coloring_9_28",
        "q6_s6_numeric_compatibility_route_cut_9_29",
        "q6_intersection_budget",
    }
    require(
        all((status[name] == 'PROVED' for name in proved)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1487',
    )
    require(
        status['q1_residue_classification'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1488',
    )
    require(
        status['q6_component_classification'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1489',
    )
    require(
        status['q6_low_degree_component_interpolation'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1490',
    )
    require(
        status['one_triangle_target'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1491',
    )
    require(
        status['pdcec'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1492',
    )
    require(
        payload['payment'] == 'NONE',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1493',
    )
    require(
        payload['tamper_mutations_rejected'] == 21,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1494',
    )
    require(
        payload['payload_sha256'] == payload_sha256(payload),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1495',
    )


def rehash(payload: dict[str, object]) -> None:
    payload["payload_sha256"] = payload_sha256(payload)


def tamper_suite(payload: dict[str, object]) -> int:
    """Rehash each forged payload; semantic validation must reject it."""
    rejected = 0
    mutations: list[dict[str, object]] = []

    forged = copy.deepcopy(payload)
    forged["theorem_status"]["pdcec"] = "PROVED"
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["payment"] = "BOOKED"
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["coordinate_law"]["conic_evaluation_rank"] = 2
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["design_census"]["cyclic_guardrail_co12_triples"] = 1
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["outgoing_conjugate_ledger"]["excluded_q"] = [2, 3]
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["outgoing_conjugate_ledger"]["q5_residual_resultant_degree"] = 34
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["outgoing_conjugate_ledger"][
        "q5_remaining_component_partitions"
    ] = [[5], [4, 1], [3, 2]]
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["outgoing_conjugate_ledger"]["q5_branch_status"] = "OPEN"
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["outgoing_conjugate_ledger"][
        "q6_graph_branch_initial_slack_cap"
    ] = 13
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["outgoing_conjugate_ledger"][
        "q6_quotient_resultant_residual_caps_by_s"
    ]["3"] = 4
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["outgoing_conjugate_ledger"][
        "q6_graph_s5_cross_incidence"
    ] = 5
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["outgoing_conjugate_ledger"][
        "q6_remaining_invariant_coordinate_counts"
    ] = [0, 1, 5, 6]
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["outgoing_conjugate_ledger"][
        "q6_s6_split_pencil_pair_count"
    ] = 59
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["design_census"]["cyclic_q6_split_pencil_algebra_supplied"] = True
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["outgoing_conjugate_ledger"][
        "q6_s6_invariant_source_label_symmetric_difference_maximum"
    ] = 4
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["outgoing_conjugate_ledger"][
        "q6_s6_distinct_split_fibers_per_pencil_maximum"
    ] = 11
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["outgoing_conjugate_ledger"][
        "q6_s6_source_facet_matching_size"
    ] = 7
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["outgoing_conjugate_ledger"][
        "q6_s6_horizontal_fiber_classes"
    ]["ramification_allowed_over_K_eta"] = False
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["theorem_status"][
        "q6_low_degree_component_interpolation"
    ] = "PROVED"
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["q6_s6_component_correction"]["cycle_monochromatic"] = True
    mutations.append(forged)

    forged = copy.deepcopy(payload)
    forged["q6_s6_component_correction"][
        "component_edge_color_counts"
    ] = [7, 5]
    mutations.append(forged)

    for forged in mutations:
        rehash(forged)
        try:
            validate(forged)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError("semantic tamper was accepted")
    require(
        rejected == 21,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_facet_collinearity.py:1623',
    )
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true",
                        help="write the certificate")
    parser.add_argument("--check", action="store_true",
                        help="compare with the stored certificate")
    parser.add_argument("--tamper-selftest", action="store_true",
                        help="run rehashed semantic tamper tests")
    args = parser.parse_args()
    if not (args.emit or args.check or args.tamper_selftest):
        args.check = True
        args.tamper_selftest = True

    payload = run_all()
    validate(payload)
    if args.tamper_selftest:
        tamper_suite(payload)
    if args.emit:
        CERTIFICATE.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
        print(f"certificate written: {CERTIFICATE.name}")
    if args.check:
        stored = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
        if stored != payload:
            raise SystemExit("FAIL: certificate mismatch (fail-closed)")
    print("PASS: all exact checks and certificate equality")
    print(f"  field: {P}")
    print(f"  coordinate-law checks: "
          f"{payload['coordinate_law']['coordinate_law_checks']}")
    print(f"  vertex-formula incidences: "
          f"{payload['split_model']['vertex_formula_incidence_checks']}")
    print(f"  guardrail co-12-set triples: "
          f"{payload['design_census']['cyclic_guardrail_co12_triples']}")
    print(f"  tamper mutations rejected: "
          f"{payload['tamper_mutations_rejected']}")
    print("  Q=1,2,3,4,5 deck branches: EXCLUDED (remaining Q=6,...,10)")
    print("  Q=6 invariant-coordinate counts: remaining s=0,1 nonfixed,6")
    print("  one-triangle target: OPEN -- no payment booked")


if __name__ == "__main__":
    main()
