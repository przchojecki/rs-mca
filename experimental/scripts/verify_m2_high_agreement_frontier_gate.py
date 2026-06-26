#!/usr/bin/env python3
"""Verify row-level consequences of the high-agreement tangent staircase.

This is an arithmetic/audit verifier.  It does not reprove the tangent
staircase.  It checks how the exact identity

    LD_sw(C,a) = n-a+1     for a >= ceil((2n+k)/3)

and its projective tangent-star corollary interact with the integer target
budgets floor(q_line / 2^eps_bits) and floor((q_line+1) / 2^eps_bits).
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from itertools import combinations, product
from typing import Any


@dataclass(frozen=True)
class Gate:
    label: str
    n: int
    k: int
    q_line: int
    eps_bits: int
    target_unit: int
    q_line_window: str
    projective_q_line_window: str
    exact_start: int
    exact_distance_limit: int
    lower_floor_distance_limit: int
    budget: int
    projective_budget: int
    exact_start_count: int
    projective_last_safe_distance_in_exact_range: int | None
    projective_first_unsafe_distance_in_exact_range: int | None
    status: str
    last_unsafe_agreement: int | None
    first_safe_agreement: int | None
    last_unsafe_distance: int | None
    first_safe_distance: int | None
    first_unsafe_grid_radius: str | None
    largest_safe_grid_radius: str | None
    projective_status: str
    projective_last_unsafe_agreement: int | None
    projective_first_safe_agreement: int | None
    projective_last_unsafe_distance: int | None
    projective_first_safe_distance: int | None
    projective_first_unsafe_grid_radius: str | None
    projective_largest_safe_grid_radius: str | None


def ceil_div(num: int, den: int) -> int:
    return -(-num // den)


def q_line_window(n: int, k: int, q_line: int, eps_bits: int) -> str:
    target_unit = 1 << eps_bits
    return budget_window(
        q_line // target_unit, (n - k) // 3, n - k - 1
    )


def projective_q_line_window(n: int, k: int, q_line: int, eps_bits: int) -> str:
    target_unit = 1 << eps_bits
    return budget_window(
        (q_line + 1) // target_unit, (n - k) // 3, n - k - 1
    )


def budget_window(
    budget: int, exact_distance_limit: int, lower_floor_distance_limit: int
) -> str:
    if budget == 0:
        return "budget_zero_q_line_window"
    if budget <= exact_distance_limit:
        return "exact_crossing_q_line_window"
    if budget <= lower_floor_distance_limit:
        return "exact_safe_then_gap_q_line_window"
    return "tangent_floor_never_crosses_q_line_window"


def threshold_summary(
    n: int,
    exact_start: int,
    exact_distance_limit: int,
    lower_floor_distance_limit: int,
    budget: int,
) -> tuple[str, int | None, int | None, int | None, int | None, str | None, str | None]:
    if budget == 0:
        return (
            "no_safe_agreement_in_exact_tangent_range",
            n,
            None,
            0,
            None,
            "0",
            None,
        )

    if budget <= exact_distance_limit:
        first_safe = n - budget + 1
        last_unsafe = first_safe - 1
        return (
            "crossing_inside_exact_tangent_range",
            last_unsafe,
            first_safe,
            n - last_unsafe,
            n - first_safe,
            str(Fraction(n - last_unsafe, n)),
            str(Fraction(n - first_safe, n)),
        )

    if budget <= lower_floor_distance_limit:
        unsafe_agreement = n - budget
        return (
            "safe_exact_range_then_tangent_unsafe_floor",
            unsafe_agreement,
            exact_start,
            budget,
            exact_distance_limit,
            str(Fraction(budget, n)),
            str(Fraction(exact_distance_limit, n)),
        )

    return (
        "tangent_floor_never_crosses_budget",
        None,
        exact_start,
        None,
        n - exact_start,
        None,
        str(Fraction(n - exact_start, n)),
    )


def q_line_window_bounds(
    budget: int, target_unit: int, offset: int
) -> tuple[int, int]:
    return budget * target_unit - offset, (budget + 1) * target_unit - offset


def assert_q_line_budget_window(
    q_line: int, budget: int, target_unit: int, offset: int
) -> None:
    lower, upper = q_line_window_bounds(budget, target_unit, offset)
    assert lower <= q_line < upper


def projective_exact_distances(
    exact_distance_limit: int, projective_budget: int
) -> tuple[int | None, int | None]:
    """Projective exact range has LD_sw^P(C,n-d)=d+1."""

    last_safe = None
    if projective_budget >= 1:
        last_safe = min(exact_distance_limit, projective_budget - 1)
    first_unsafe = projective_budget
    if not (0 <= first_unsafe <= exact_distance_limit):
        first_unsafe = None
    return last_safe, first_unsafe


def challenge_pullback_probability(
    challenge_to_slope: list[Any], bad_slopes: set[Any]
) -> Fraction:
    if not challenge_to_slope:
        raise ValueError("expected at least one challenge")
    bad_challenges = sum(1 for slope in challenge_to_slope if slope in bad_slopes)
    return Fraction(bad_challenges, len(challenge_to_slope))


def fiber_sizes_descending(challenge_to_slope: list[Any]) -> list[int]:
    if not challenge_to_slope:
        raise ValueError("expected at least one challenge")
    fibers: dict[Any, int] = {}
    for slope in challenge_to_slope:
        fibers[slope] = fibers.get(slope, 0) + 1
    return sorted(fibers.values(), reverse=True)


def max_fiber_size(challenge_to_slope: list[Any]) -> int:
    return fiber_sizes_descending(challenge_to_slope)[0]


def adversarial_fiber_envelope(
    challenge_to_slope: list[Any], bad_count: int
) -> Fraction:
    if bad_count < 0:
        raise ValueError("expected nonnegative bad_count")
    fibers = fiber_sizes_descending(challenge_to_slope)
    return Fraction(sum(fibers[:bad_count]), len(challenge_to_slope))


def brute_adversarial_fiber_envelope(
    challenge_to_slope: list[Any], bad_count: int
) -> Fraction:
    if not challenge_to_slope:
        raise ValueError("expected at least one challenge")
    if bad_count < 0:
        raise ValueError("expected nonnegative bad_count")
    slopes = list(set(challenge_to_slope))
    best = Fraction(0, 1)
    for size in range(min(bad_count, len(slopes)) + 1):
        for bad_tuple in combinations(slopes, size):
            best = max(
                best,
                challenge_pullback_probability(challenge_to_slope, set(bad_tuple)),
            )
    return best


def matrix_rank_mod(matrix: list[list[int]], prime: int) -> int:
    if prime <= 1:
        raise ValueError("expected prime > 1")
    if not matrix:
        return 0
    width = len(matrix[0])
    rows = [[entry % prime for entry in row] for row in matrix]
    for row in rows:
        if len(row) != width:
            raise ValueError("ragged matrix")

    rank = 0
    for col in range(width):
        pivot = None
        for row_idx in range(rank, len(rows)):
            if rows[row_idx][col] != 0:
                pivot = row_idx
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, prime)
        rows[rank] = [(entry * inv) % prime for entry in rows[rank]]
        for row_idx in range(len(rows)):
            if row_idx == rank or rows[row_idx][col] == 0:
                continue
            factor = rows[row_idx][col]
            rows[row_idx] = [
                (entry - factor * pivot_entry) % prime
                for entry, pivot_entry in zip(rows[row_idx], rows[rank])
            ]
        rank += 1
        if rank == len(rows):
            break
    return rank


def linear_map_values(matrix: list[list[int]], prime: int) -> list[tuple[int, ...]]:
    if not matrix:
        raise ValueError("expected at least one output row")
    domain_dim = len(matrix[0])
    for row in matrix:
        if len(row) != domain_dim:
            raise ValueError("ragged matrix")

    values: list[tuple[int, ...]] = []
    for vector in product(range(prime), repeat=domain_dim):
        image = tuple(
            sum(row[col] * vector[col] for col in range(domain_dim)) % prime
            for row in matrix
        )
        values.append(image)
    return values


def challenge_pullback_bound(
    challenge_count: int, bad_count: int, max_fiber: int
) -> Fraction:
    if challenge_count <= 0:
        raise ValueError("expected positive challenge_count")
    if bad_count < 0:
        raise ValueError("expected nonnegative bad_count")
    if max_fiber <= 0:
        raise ValueError("expected positive max_fiber")
    return Fraction(min(challenge_count, bad_count * max_fiber), challenge_count)


def poly_eval_mod(coeffs: list[int], x: int, prime: int) -> int:
    total = 0
    power = 1
    for coeff in coeffs:
        total = (total + coeff * power) % prime
        power = (power * x) % prime
    return total


def poly_degree(coeffs: list[int]) -> int:
    for idx in range(len(coeffs) - 1, -1, -1):
        if coeffs[idx] != 0:
            return idx
    raise ValueError("zero polynomial has no degree")


def polynomial_map_values(coeffs: list[int], prime: int) -> list[int]:
    degree = poly_degree([c % prime for c in coeffs])
    if degree <= 0:
        raise ValueError("expected nonconstant polynomial")
    return [poly_eval_mod(coeffs, x, prime) for x in range(prime)]


def rational_map_values(
    numerator: list[int], denominator: list[int], prime: int
) -> list[int | str]:
    degree = max(
        poly_degree([c % prime for c in numerator]),
        poly_degree([c % prime for c in denominator]),
    )
    if degree <= 0:
        raise ValueError("expected nonconstant rational map")
    values: list[int | str] = []
    for x in range(prime):
        den = poly_eval_mod(denominator, x, prime)
        if den == 0:
            values.append("inf")
        else:
            num = poly_eval_mod(numerator, x, prime)
            values.append((num * pow(den, -1, prime)) % prime)
    return values


def tangent_gate(label: str, n: int, k: int, q_line: int, eps_bits: int) -> Gate:
    if not (0 <= k < n):
        raise ValueError("expected 0 <= k < n")
    if q_line <= 0:
        raise ValueError("expected positive q_line")
    if eps_bits < 0:
        raise ValueError("expected nonnegative eps_bits")

    target_unit = 1 << eps_bits
    exact_start = ceil_div(2 * n + k, 3)
    exact_distance_limit = (n - k) // 3
    lower_floor_distance_limit = n - k - 1
    assert exact_start == n - exact_distance_limit
    assert k + 1 <= exact_start <= n
    exact_start_count = n - exact_start + 1
    assert exact_start_count == exact_distance_limit + 1
    budget = q_line // target_unit
    projective_budget = (q_line + 1) // target_unit
    window = q_line_window(n, k, q_line, eps_bits)
    projective_window = projective_q_line_window(n, k, q_line, eps_bits)

    projective_last_safe, projective_first_unsafe = projective_exact_distances(
        exact_distance_limit, projective_budget
    )

    (
        status,
        last_unsafe_agreement,
        first_safe_agreement,
        last_unsafe_distance,
        first_safe_distance,
        first_unsafe_grid_radius,
        largest_safe_grid_radius,
    ) = threshold_summary(
        n, exact_start, exact_distance_limit, lower_floor_distance_limit, budget
    )
    (
        projective_status,
        projective_last_unsafe_agreement,
        projective_first_safe_agreement,
        projective_last_unsafe_distance,
        projective_first_safe_distance,
        projective_first_unsafe_grid_radius,
        projective_largest_safe_grid_radius,
    ) = threshold_summary(
        n,
        exact_start,
        exact_distance_limit,
        lower_floor_distance_limit,
        projective_budget,
    )

    return Gate(
        label=label,
        n=n,
        k=k,
        q_line=q_line,
        eps_bits=eps_bits,
        target_unit=target_unit,
        q_line_window=window,
        projective_q_line_window=projective_window,
        exact_start=exact_start,
        exact_distance_limit=exact_distance_limit,
        lower_floor_distance_limit=lower_floor_distance_limit,
        budget=budget,
        projective_budget=projective_budget,
        exact_start_count=exact_start_count,
        projective_last_safe_distance_in_exact_range=projective_last_safe,
        projective_first_unsafe_distance_in_exact_range=projective_first_unsafe,
        status=status,
        last_unsafe_agreement=last_unsafe_agreement,
        first_safe_agreement=first_safe_agreement,
        last_unsafe_distance=last_unsafe_distance,
        first_safe_distance=first_safe_distance,
        first_unsafe_grid_radius=first_unsafe_grid_radius,
        largest_safe_grid_radius=largest_safe_grid_radius,
        projective_status=projective_status,
        projective_last_unsafe_agreement=projective_last_unsafe_agreement,
        projective_first_safe_agreement=projective_first_safe_agreement,
        projective_last_unsafe_distance=projective_last_unsafe_distance,
        projective_first_safe_distance=projective_first_safe_distance,
        projective_first_unsafe_grid_radius=projective_first_unsafe_grid_radius,
        projective_largest_safe_grid_radius=projective_largest_safe_grid_radius,
    )


def active_row() -> Gate:
    return tangent_gate(
        label="F_17^32 n=512 k=256",
        n=512,
        k=256,
        q_line=17**32,
        eps_bits=128,
    )


def check_gate(gate: Gate) -> None:
    assert gate.target_unit == 1 << gate.eps_bits
    assert gate.q_line_window == q_line_window(
        gate.n, gate.k, gate.q_line, gate.eps_bits
    )
    assert gate.projective_q_line_window == projective_q_line_window(
        gate.n, gate.k, gate.q_line, gate.eps_bits
    )
    assert gate.exact_start == ceil_div(2 * gate.n + gate.k, 3)
    assert gate.exact_distance_limit == (gate.n - gate.k) // 3
    assert gate.lower_floor_distance_limit == gate.n - gate.k - 1
    assert gate.exact_start == gate.n - gate.exact_distance_limit
    assert gate.exact_start_count == gate.n - gate.exact_start + 1
    assert gate.exact_start_count == gate.exact_distance_limit + 1
    for d in range(1, gate.exact_distance_limit + 1):
        assert gate.n - 2 * d - 1 >= gate.k
    assert gate.budget == gate.q_line // gate.target_unit
    assert gate.projective_budget == (gate.q_line + 1) // gate.target_unit
    assert gate.q_line_window == budget_window(
        gate.budget, gate.exact_distance_limit, gate.lower_floor_distance_limit
    )
    assert gate.projective_q_line_window == budget_window(
        gate.projective_budget,
        gate.exact_distance_limit,
        gate.lower_floor_distance_limit,
    )
    assert_q_line_budget_window(gate.q_line, gate.budget, gate.target_unit, 0)
    assert_q_line_budget_window(
        gate.q_line, gate.projective_budget, gate.target_unit, 1
    )
    expected_projective = projective_exact_distances(
        gate.exact_distance_limit, gate.projective_budget
    )
    assert (
        gate.projective_last_safe_distance_in_exact_range,
        gate.projective_first_unsafe_distance_in_exact_range,
    ) == expected_projective
    if gate.projective_last_safe_distance_in_exact_range is not None:
        d = gate.projective_last_safe_distance_in_exact_range
        assert 0 <= d <= gate.exact_distance_limit
        assert d + 1 <= gate.projective_budget
        if d < gate.exact_distance_limit:
            assert d + 2 > gate.projective_budget
    if gate.projective_first_unsafe_distance_in_exact_range is not None:
        d = gate.projective_first_unsafe_distance_in_exact_range
        assert 0 <= d <= gate.exact_distance_limit
        assert d + 1 > gate.projective_budget
        assert d == gate.projective_budget

    if gate.status == "crossing_inside_exact_tangent_range":
        assert gate.last_unsafe_agreement is not None
        assert gate.first_safe_agreement is not None
        assert gate.last_unsafe_agreement + 1 == gate.first_safe_agreement
        assert gate.last_unsafe_agreement >= gate.exact_start
        assert 1 <= gate.budget <= gate.exact_distance_limit
        assert gate.q_line_window == "exact_crossing_q_line_window"
        assert gate.target_unit <= gate.q_line
        assert gate.q_line < (gate.exact_distance_limit + 1) * gate.target_unit
        assert gate.budget * gate.target_unit <= gate.q_line
        assert gate.q_line < (gate.budget + 1) * gate.target_unit
        assert gate.n - gate.last_unsafe_agreement + 1 == gate.budget + 1
        assert gate.n - gate.first_safe_agreement + 1 == gate.budget
    elif gate.status == "safe_exact_range_then_tangent_unsafe_floor":
        assert gate.budget > gate.exact_distance_limit
        assert gate.budget <= gate.lower_floor_distance_limit
        assert gate.q_line_window == "exact_safe_then_gap_q_line_window"
        assert (gate.exact_distance_limit + 1) * gate.target_unit <= gate.q_line
        assert gate.q_line < (gate.lower_floor_distance_limit + 1) * gate.target_unit
        assert gate.budget * gate.target_unit <= gate.q_line
        assert gate.q_line < (gate.budget + 1) * gate.target_unit
        assert gate.first_safe_agreement == gate.exact_start
        assert gate.first_safe_distance == gate.exact_distance_limit
        assert gate.last_unsafe_agreement == gate.n - gate.budget
        assert gate.last_unsafe_distance == gate.budget
    elif gate.status == "tangent_floor_never_crosses_budget":
        assert gate.budget > gate.exact_distance_limit
        assert gate.budget > gate.lower_floor_distance_limit
        assert gate.budget >= gate.exact_start_count
        assert gate.q_line_window == "tangent_floor_never_crosses_q_line_window"
        assert (gate.lower_floor_distance_limit + 1) * gate.target_unit <= gate.q_line
        assert gate.first_safe_agreement == gate.exact_start
    elif gate.status == "no_safe_agreement_in_exact_tangent_range":
        assert gate.budget == 0
        assert gate.q_line_window == "budget_zero_q_line_window"
        assert 0 < gate.q_line < gate.target_unit
        assert gate.last_unsafe_agreement == gate.n
    else:
        raise AssertionError(f"unknown status {gate.status}")

    if gate.projective_status == "crossing_inside_exact_tangent_range":
        assert gate.projective_last_unsafe_agreement is not None
        assert gate.projective_first_safe_agreement is not None
        assert (
            gate.projective_last_unsafe_agreement + 1
            == gate.projective_first_safe_agreement
        )
        assert gate.projective_last_unsafe_agreement >= gate.exact_start
        assert 1 <= gate.projective_budget <= gate.exact_distance_limit
        assert gate.projective_q_line_window == "exact_crossing_q_line_window"
        assert gate.n - gate.projective_last_unsafe_agreement + 1 == (
            gate.projective_budget + 1
        )
        assert (
            gate.n - gate.projective_first_safe_agreement + 1
            == gate.projective_budget
        )
    elif gate.projective_status == "safe_exact_range_then_tangent_unsafe_floor":
        assert gate.projective_budget > gate.exact_distance_limit
        assert gate.projective_budget <= gate.lower_floor_distance_limit
        assert gate.projective_q_line_window == "exact_safe_then_gap_q_line_window"
        assert gate.projective_first_safe_agreement == gate.exact_start
        assert gate.projective_first_safe_distance == gate.exact_distance_limit
        assert gate.projective_last_unsafe_agreement == gate.n - gate.projective_budget
        assert gate.projective_last_unsafe_distance == gate.projective_budget
    elif gate.projective_status == "tangent_floor_never_crosses_budget":
        assert gate.projective_budget > gate.exact_distance_limit
        assert gate.projective_budget > gate.lower_floor_distance_limit
        assert gate.projective_q_line_window == "tangent_floor_never_crosses_q_line_window"
        assert gate.projective_first_safe_agreement == gate.exact_start
    elif gate.projective_status == "no_safe_agreement_in_exact_tangent_range":
        assert gate.projective_budget == 0
        assert gate.projective_q_line_window == "budget_zero_q_line_window"
        assert gate.projective_last_unsafe_agreement == gate.n
    else:
        raise AssertionError(f"unknown projective status {gate.projective_status}")


def check_challenge_pullback_ledger() -> None:
    identity = list(range(8))
    bad = {1, 3, 6}
    assert challenge_pullback_probability(identity, bad) == Fraction(3, 8)
    assert fiber_sizes_descending(identity) == [1] * 8
    assert max_fiber_size(identity) == 1
    assert challenge_pullback_bound(len(identity), len(bad), 1) == Fraction(3, 8)

    two_to_one = [0, 0, 1, 1, 2, 2, 3, 3]
    bad = {1, 3}
    assert challenge_pullback_probability(two_to_one, bad) == Fraction(1, 2)
    assert fiber_sizes_descending(two_to_one) == [2, 2, 2, 2]
    assert max_fiber_size(two_to_one) == 2
    assert challenge_pullback_bound(len(two_to_one), len(bad), 2) == Fraction(1, 2)

    constant = [5] * 8
    bad = {5}
    assert challenge_pullback_probability(constant, bad) == Fraction(1, 1)
    assert fiber_sizes_descending(constant) == [8]
    assert max_fiber_size(constant) == 8
    assert challenge_pullback_bound(len(constant), len(bad), 8) == Fraction(1, 1)

    active = active_row()
    assert challenge_pullback_bound(
        active.q_line, active.budget, 1
    ) == Fraction(active.budget, active.q_line)
    assert challenge_pullback_bound(
        active.q_line + 1, active.projective_budget, 1
    ) == Fraction(active.projective_budget, active.q_line + 1)


def check_adversarial_fiber_envelope() -> None:
    identity = list(range(8))
    assert adversarial_fiber_envelope(identity, 3) == Fraction(3, 8)
    assert adversarial_fiber_envelope(identity, 3) == brute_adversarial_fiber_envelope(
        identity, 3
    )

    two_to_one = [0, 0, 1, 1, 2, 2, 3, 3]
    assert adversarial_fiber_envelope(two_to_one, 2) == Fraction(1, 2)
    assert adversarial_fiber_envelope(two_to_one, 2) == (
        brute_adversarial_fiber_envelope(two_to_one, 2)
    )

    nonuniform = [0, 0, 0, 1, 1, 2, 3, 4]
    assert fiber_sizes_descending(nonuniform) == [3, 2, 1, 1, 1]
    assert adversarial_fiber_envelope(nonuniform, 2) == Fraction(5, 8)
    assert adversarial_fiber_envelope(nonuniform, 2) == (
        brute_adversarial_fiber_envelope(nonuniform, 2)
    )
    assert challenge_pullback_bound(8, 2, max_fiber_size(nonuniform)) == Fraction(3, 4)

    constant = [5] * 8
    assert adversarial_fiber_envelope(constant, 1) == Fraction(1, 1)
    assert adversarial_fiber_envelope(constant, 1) == (
        brute_adversarial_fiber_envelope(constant, 1)
    )

    # A uniform projection from a larger challenge set to base slopes recovers
    # the base-slope denominator, not the larger challenge denominator.
    prime = 5
    extension_degree = 3
    uniform_projection = [x % prime for x in range(prime**extension_degree)]
    assert len(uniform_projection) == prime**extension_degree
    assert fiber_sizes_descending(uniform_projection) == [
        prime ** (extension_degree - 1)
    ] * prime
    assert adversarial_fiber_envelope(uniform_projection, 2) == Fraction(2, prime)
    assert challenge_pullback_bound(
        len(uniform_projection), 2, max_fiber_size(uniform_projection)
    ) == Fraction(2, prime)


def check_linear_challenge_map_ledger() -> None:
    prime = 5

    rank_one_projection = [[1, 0, 0]]
    rank_one_values = linear_map_values(rank_one_projection, prime)
    rank_one = matrix_rank_mod(rank_one_projection, prime)
    assert rank_one == 1
    assert len(rank_one_values) == prime**3
    assert fiber_sizes_descending(rank_one_values) == [prime**2] * prime
    assert adversarial_fiber_envelope(rank_one_values, 2) == Fraction(2, prime)
    assert challenge_pullback_bound(
        len(rank_one_values), 2, max_fiber_size(rank_one_values)
    ) == Fraction(2, prime**rank_one)

    rank_two_projection = [[1, 0, 0], [0, 1, 0]]
    rank_two_values = linear_map_values(rank_two_projection, prime)
    rank_two = matrix_rank_mod(rank_two_projection, prime)
    assert rank_two == 2
    assert fiber_sizes_descending(rank_two_values) == [prime] * (prime**2)
    assert adversarial_fiber_envelope(rank_two_values, 3) == Fraction(3, prime**2)
    assert challenge_pullback_bound(
        len(rank_two_values), 3, max_fiber_size(rank_two_values)
    ) == Fraction(3, prime**rank_two)

    full_rank = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    full_rank_values = linear_map_values(full_rank, prime)
    rank_three = matrix_rank_mod(full_rank, prime)
    assert rank_three == 3
    assert max_fiber_size(full_rank_values) == 1
    assert adversarial_fiber_envelope(full_rank_values, 4) == Fraction(4, prime**3)
    assert challenge_pullback_bound(
        len(full_rank_values), 4, max_fiber_size(full_rank_values)
    ) == Fraction(4, prime**rank_three)

    dependent_rows = [[1, 2, 0], [2, 4, 0], [0, 0, 1]]
    dependent_values = linear_map_values(dependent_rows, prime)
    dependent_rank = matrix_rank_mod(dependent_rows, prime)
    assert dependent_rank == 2
    assert fiber_sizes_descending(dependent_values) == [prime] * (prime**2)
    assert adversarial_fiber_envelope(dependent_values, 5) == Fraction(1, prime)


def check_rational_challenge_map_degree_ledger() -> None:
    prime = 17

    # phi(x)=x^3+2x+1 has degree 3, so every fiber has size at most 3.
    polynomial_values = polynomial_map_values([1, 2, 0, 1], prime)
    polynomial_degree = 3
    polynomial_fiber = max_fiber_size(polynomial_values)
    assert polynomial_fiber <= polynomial_degree
    polynomial_bad = {polynomial_values[0], polynomial_values[5]}
    assert challenge_pullback_probability(
        polynomial_values, polynomial_bad
    ) <= challenge_pullback_bound(prime, len(polynomial_bad), polynomial_degree)
    assert adversarial_fiber_envelope(
        polynomial_values, len(polynomial_bad)
    ) <= challenge_pullback_bound(prime, len(polynomial_bad), polynomial_degree)

    # phi(x)=(x^2+1)/(x-3) maps to P^1(F_17) and has degree 2.
    rational_values = rational_map_values([1, 0, 1], [-3, 1], prime)
    rational_degree = 2
    rational_fiber = max_fiber_size(rational_values)
    assert rational_fiber <= rational_degree
    rational_bad = {rational_values[4], "inf"}
    assert challenge_pullback_probability(
        rational_values, rational_bad
    ) <= challenge_pullback_bound(prime, len(rational_bad), rational_degree)
    assert adversarial_fiber_envelope(
        rational_values, len(rational_bad)
    ) <= challenge_pullback_bound(prime, len(rational_bad), rational_degree)

    # A constant map shows why nonconstancy is necessary for a degree ledger.
    constant_values = [9] * prime
    assert max_fiber_size(constant_values) == prime
    assert challenge_pullback_probability(constant_values, {9}) == Fraction(1, 1)


def default_cases() -> list[Gate]:
    return [
        active_row(),
        tangent_gate(
            label="toy crossing inside exact range",
            n=20,
            k=8,
            q_line=3,
            eps_bits=0,
        ),
        tangent_gate(
            label="toy crossing at exact-range boundary",
            n=20,
            k=8,
            q_line=4,
            eps_bits=0,
        ),
        tangent_gate(
            label="toy exact-safe plus tangent-unsafe gap",
            n=20,
            k=8,
            q_line=8,
            eps_bits=0,
        ),
        tangent_gate(
            label="toy tangent floor never crosses",
            n=20,
            k=8,
            q_line=16,
            eps_bits=0,
        ),
        tangent_gate(
            label="toy budget zero",
            n=20,
            k=8,
            q_line=7,
            eps_bits=3,
        ),
        tangent_gate(
            label="toy finite and projective budget zero",
            n=20,
            k=8,
            q_line=6,
            eps_bits=3,
        ),
    ]


def print_human(gates: list[Gate]) -> None:
    for gate in gates:
        print(gate.label)
        print(f"  n={gate.n} k={gate.k}")
        print(f"  q_line={gate.q_line}")
        print(f"  eps_bits={gate.eps_bits}")
        print(f"  target_unit=2^eps_bits={gate.target_unit}")
        print(f"  q_line_window={gate.q_line_window}")
        print(f"  projective_q_line_window={gate.projective_q_line_window}")
        print(f"  exact_start={gate.exact_start}")
        print(f"  exact_distance_limit={gate.exact_distance_limit}")
        print(f"  lower_floor_distance_limit={gate.lower_floor_distance_limit}")
        print(f"  exact_start_count={gate.exact_start_count}")
        print(f"  budget=floor(q_line/2^eps_bits)={gate.budget}")
        print(f"  projective_budget=floor((q_line+1)/2^eps_bits)={gate.projective_budget}")
        print(f"  status={gate.status}")
        print(f"  projective_status={gate.projective_status}")
        if gate.last_unsafe_agreement is not None:
            print(
                "  last_unsafe_agreement="
                f"{gate.last_unsafe_agreement}, distance={gate.last_unsafe_distance}, "
                f"grid_radius={gate.first_unsafe_grid_radius}"
            )
        if gate.first_safe_agreement is not None:
            print(
                "  first_safe_agreement="
                f"{gate.first_safe_agreement}, distance={gate.first_safe_distance}, "
                f"grid_radius={gate.largest_safe_grid_radius}"
            )
        if gate.status == "crossing_inside_exact_tangent_range":
            print(
                "  closed_ball_safe_condition="
                f"delta < {gate.first_unsafe_grid_radius}"
            )
            print(
                "  strict_ball_safe_endpoint="
                f"delta = {gate.first_unsafe_grid_radius}"
            )
        if gate.status == "safe_exact_range_then_tangent_unsafe_floor":
            gap_start = gate.exact_distance_limit + 1
            gap_end = gate.budget - 1
            print(f"  unresolved_distance_gap={gap_start}..{gap_end}")
        if gate.projective_last_safe_distance_in_exact_range is not None:
            print(
                "  projective_exact_range_safe_through_distance="
                f"{gate.projective_last_safe_distance_in_exact_range}"
            )
        if gate.projective_first_unsafe_distance_in_exact_range is not None:
            print(
                "  projective_exact_range_unsafe_from_distance="
                f"{gate.projective_first_unsafe_distance_in_exact_range}"
            )
        if gate.projective_last_unsafe_agreement is not None:
            print(
                "  projective_last_unsafe_agreement="
                f"{gate.projective_last_unsafe_agreement}, "
                f"distance={gate.projective_last_unsafe_distance}, "
                f"grid_radius={gate.projective_first_unsafe_grid_radius}"
            )
        if gate.projective_first_safe_agreement is not None:
            print(
                "  projective_first_safe_agreement="
                f"{gate.projective_first_safe_agreement}, "
                f"distance={gate.projective_first_safe_distance}, "
                f"grid_radius={gate.projective_largest_safe_grid_radius}"
            )
        print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int)
    parser.add_argument("--k", type=int)
    parser.add_argument("--q-line", type=int)
    parser.add_argument("--eps-bits", type=int, default=128)
    parser.add_argument("--label", default="custom")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    custom = args.n is not None or args.k is not None or args.q_line is not None
    if custom:
        if args.n is None or args.k is None or args.q_line is None:
            raise SystemExit("--n, --k, and --q-line must be supplied together")
        gates = [tangent_gate(args.label, args.n, args.k, args.q_line, args.eps_bits)]
    else:
        gates = default_cases()

    for gate in gates:
        check_gate(gate)
    check_challenge_pullback_ledger()
    check_adversarial_fiber_envelope()
    check_linear_challenge_map_ledger()
    check_rational_challenge_map_degree_ledger()

    active = gates[0] if not custom else None
    if active is not None:
        assert active.exact_start == 427
        assert active.exact_distance_limit == 85
        assert active.lower_floor_distance_limit == 255
        assert active.budget == 6
        assert active.projective_budget == 6
        assert active.target_unit == 1 << 128
        assert active.q_line_window == "exact_crossing_q_line_window"
        assert active.projective_q_line_window == "exact_crossing_q_line_window"
        assert 6 * active.target_unit <= active.q_line
        assert active.q_line < 7 * active.target_unit
        assert 6 * active.target_unit - 1 <= active.q_line
        assert active.q_line < 7 * active.target_unit - 1
        assert active.projective_last_safe_distance_in_exact_range == 5
        assert active.projective_first_unsafe_distance_in_exact_range == 6
        assert active.status == "crossing_inside_exact_tangent_range"
        assert active.projective_status == "crossing_inside_exact_tangent_range"
        assert active.last_unsafe_agreement == 506
        assert active.first_safe_agreement == 507
        assert active.projective_last_unsafe_agreement == 506
        assert active.projective_first_safe_agreement == 507
        assert active.last_unsafe_distance == 6
        assert active.first_safe_distance == 5
        assert active.projective_last_unsafe_distance == 6
        assert active.projective_first_safe_distance == 5
        assert active.first_unsafe_grid_radius == "3/256"
        assert active.largest_safe_grid_radius == "5/512"
        assert active.projective_first_unsafe_grid_radius == "3/256"
        assert active.projective_largest_safe_grid_radius == "5/512"

    if args.json:
        payload: list[dict[str, Any]] = [asdict(gate) for gate in gates]
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_human(gates)
        print("m2_high_agreement_frontier_gate: PASS")


if __name__ == "__main__":
    main()
