#!/usr/bin/env python3
"""Verify row-level consequences of the high-agreement tangent staircase.

This is an arithmetic/audit verifier.  It does not reprove the tangent
staircase.  It checks how the exact identity

    LD_sw(C,a) = n-a+1     for a >= ceil((2n+k)/3)

interacts with an integer target budget floor(q_line / 2^eps_bits).
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from fractions import Fraction
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
    exact_start: int
    exact_distance_limit: int
    lower_floor_distance_limit: int
    budget: int
    projective_budget: int
    exact_start_count: int
    projective_safe_distance_in_exact_range: int | None
    projective_ambiguous_distance_in_exact_range: int | None
    projective_unsafe_distance_in_exact_range: int | None
    status: str
    last_unsafe_agreement: int | None
    first_safe_agreement: int | None
    last_unsafe_distance: int | None
    first_safe_distance: int | None
    first_unsafe_grid_radius: str | None
    largest_safe_grid_radius: str | None


def ceil_div(num: int, den: int) -> int:
    return -(-num // den)


def q_line_window(n: int, k: int, q_line: int, eps_bits: int) -> str:
    target_unit = 1 << eps_bits
    exact_distance_limit = (n - k) // 3
    lower_floor_distance_limit = n - k - 1
    if q_line < target_unit:
        return "budget_zero_q_line_window"
    if q_line < (exact_distance_limit + 1) * target_unit:
        return "exact_crossing_q_line_window"
    if q_line < (lower_floor_distance_limit + 1) * target_unit:
        return "exact_safe_then_gap_q_line_window"
    return "tangent_floor_never_crosses_q_line_window"


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

    projective_safe = None
    if projective_budget >= 2:
        projective_safe = min(exact_distance_limit, projective_budget - 2)
    projective_ambiguous = projective_budget - 1
    if not (0 <= projective_ambiguous <= exact_distance_limit):
        projective_ambiguous = None
    projective_unsafe = projective_budget
    if not (0 <= projective_unsafe <= exact_distance_limit):
        projective_unsafe = None

    if budget == 0:
        status = "no_safe_agreement_in_exact_tangent_range"
        return Gate(
            label=label,
            n=n,
            k=k,
            q_line=q_line,
            eps_bits=eps_bits,
            target_unit=target_unit,
            q_line_window=window,
            exact_start=exact_start,
            exact_distance_limit=exact_distance_limit,
            lower_floor_distance_limit=lower_floor_distance_limit,
            budget=budget,
            projective_budget=projective_budget,
            exact_start_count=exact_start_count,
            projective_safe_distance_in_exact_range=projective_safe,
            projective_ambiguous_distance_in_exact_range=projective_ambiguous,
            projective_unsafe_distance_in_exact_range=projective_unsafe,
            status=status,
            last_unsafe_agreement=n,
            first_safe_agreement=None,
            last_unsafe_distance=0,
            first_safe_distance=None,
            first_unsafe_grid_radius="0",
            largest_safe_grid_radius=None,
        )

    if budget < exact_start_count:
        first_safe = n - budget + 1
        last_unsafe = first_safe - 1
        assert last_unsafe >= exact_start
        assert n - last_unsafe + 1 == budget + 1
        assert n - first_safe + 1 == budget
        return Gate(
            label=label,
            n=n,
            k=k,
            q_line=q_line,
            eps_bits=eps_bits,
            target_unit=target_unit,
            q_line_window=window,
            exact_start=exact_start,
            exact_distance_limit=exact_distance_limit,
            lower_floor_distance_limit=lower_floor_distance_limit,
            budget=budget,
            projective_budget=projective_budget,
            exact_start_count=exact_start_count,
            projective_safe_distance_in_exact_range=projective_safe,
            projective_ambiguous_distance_in_exact_range=projective_ambiguous,
            projective_unsafe_distance_in_exact_range=projective_unsafe,
            status="crossing_inside_exact_tangent_range",
            last_unsafe_agreement=last_unsafe,
            first_safe_agreement=first_safe,
            last_unsafe_distance=n - last_unsafe,
            first_safe_distance=n - first_safe,
            first_unsafe_grid_radius=str(Fraction(n - last_unsafe, n)),
            largest_safe_grid_radius=str(Fraction(n - first_safe, n)),
        )

    if budget <= lower_floor_distance_limit:
        unsafe_agreement = n - budget
        return Gate(
            label=label,
            n=n,
            k=k,
            q_line=q_line,
            eps_bits=eps_bits,
            target_unit=target_unit,
            q_line_window=window,
            exact_start=exact_start,
            exact_distance_limit=exact_distance_limit,
            lower_floor_distance_limit=lower_floor_distance_limit,
            budget=budget,
            projective_budget=projective_budget,
            exact_start_count=exact_start_count,
            projective_safe_distance_in_exact_range=projective_safe,
            projective_ambiguous_distance_in_exact_range=projective_ambiguous,
            projective_unsafe_distance_in_exact_range=projective_unsafe,
            status="safe_exact_range_then_tangent_unsafe_floor",
            last_unsafe_agreement=unsafe_agreement,
            first_safe_agreement=exact_start,
            last_unsafe_distance=budget,
            first_safe_distance=exact_distance_limit,
            first_unsafe_grid_radius=str(Fraction(budget, n)),
            largest_safe_grid_radius=str(Fraction(exact_distance_limit, n)),
        )

    return Gate(
        label=label,
        n=n,
        k=k,
        q_line=q_line,
        eps_bits=eps_bits,
        target_unit=target_unit,
        q_line_window=window,
        exact_start=exact_start,
        exact_distance_limit=exact_distance_limit,
        lower_floor_distance_limit=lower_floor_distance_limit,
        budget=budget,
        projective_budget=projective_budget,
        exact_start_count=exact_start_count,
        projective_safe_distance_in_exact_range=projective_safe,
        projective_ambiguous_distance_in_exact_range=projective_ambiguous,
        projective_unsafe_distance_in_exact_range=projective_unsafe,
        status="tangent_floor_never_crosses_budget",
        last_unsafe_agreement=None,
        first_safe_agreement=exact_start,
        last_unsafe_distance=None,
        first_safe_distance=n - exact_start,
        first_unsafe_grid_radius=None,
        largest_safe_grid_radius=str(Fraction(n - exact_start, n)),
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
    assert gate.exact_start == ceil_div(2 * gate.n + gate.k, 3)
    assert gate.exact_distance_limit == (gate.n - gate.k) // 3
    assert gate.lower_floor_distance_limit == gate.n - gate.k - 1
    assert gate.exact_start == gate.n - gate.exact_distance_limit
    assert gate.exact_start_count == gate.n - gate.exact_start + 1
    assert gate.exact_start_count == gate.exact_distance_limit + 1
    assert gate.budget == gate.q_line // gate.target_unit
    assert gate.projective_budget == (gate.q_line + 1) // gate.target_unit
    if gate.projective_safe_distance_in_exact_range is not None:
        d = gate.projective_safe_distance_in_exact_range
        assert 0 <= d <= gate.exact_distance_limit
        assert d + 2 <= gate.projective_budget
    if gate.projective_ambiguous_distance_in_exact_range is not None:
        d = gate.projective_ambiguous_distance_in_exact_range
        assert 0 <= d <= gate.exact_distance_limit
        assert d + 1 == gate.projective_budget
    if gate.projective_unsafe_distance_in_exact_range is not None:
        d = gate.projective_unsafe_distance_in_exact_range
        assert 0 <= d <= gate.exact_distance_limit
        assert d + 1 > gate.projective_budget

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
    ]


def print_human(gates: list[Gate]) -> None:
    for gate in gates:
        print(gate.label)
        print(f"  n={gate.n} k={gate.k}")
        print(f"  q_line={gate.q_line}")
        print(f"  eps_bits={gate.eps_bits}")
        print(f"  target_unit=2^eps_bits={gate.target_unit}")
        print(f"  q_line_window={gate.q_line_window}")
        print(f"  exact_start={gate.exact_start}")
        print(f"  exact_distance_limit={gate.exact_distance_limit}")
        print(f"  lower_floor_distance_limit={gate.lower_floor_distance_limit}")
        print(f"  exact_start_count={gate.exact_start_count}")
        print(f"  budget=floor(q_line/2^eps_bits)={gate.budget}")
        print(f"  projective_budget=floor((q_line+1)/2^eps_bits)={gate.projective_budget}")
        print(f"  status={gate.status}")
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
        if gate.projective_safe_distance_in_exact_range is not None:
            print(
                "  projective_exact_range_safe_through_distance="
                f"{gate.projective_safe_distance_in_exact_range}"
            )
        if gate.projective_ambiguous_distance_in_exact_range is not None:
            print(
                "  projective_exact_range_ambiguous_distance="
                f"{gate.projective_ambiguous_distance_in_exact_range}"
            )
        if gate.projective_unsafe_distance_in_exact_range is not None:
            print(
                "  projective_exact_range_unsafe_from_distance="
                f"{gate.projective_unsafe_distance_in_exact_range}"
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

    active = gates[0] if not custom else None
    if active is not None:
        assert active.exact_start == 427
        assert active.exact_distance_limit == 85
        assert active.lower_floor_distance_limit == 255
        assert active.budget == 6
        assert active.projective_budget == 6
        assert active.target_unit == 1 << 128
        assert active.q_line_window == "exact_crossing_q_line_window"
        assert 6 * active.target_unit <= active.q_line
        assert active.q_line < 7 * active.target_unit
        assert active.projective_safe_distance_in_exact_range == 4
        assert active.projective_ambiguous_distance_in_exact_range == 5
        assert active.projective_unsafe_distance_in_exact_range == 6
        assert active.status == "crossing_inside_exact_tangent_range"
        assert active.last_unsafe_agreement == 506
        assert active.first_safe_agreement == 507
        assert active.last_unsafe_distance == 6
        assert active.first_safe_distance == 5
        assert active.first_unsafe_grid_radius == "3/256"
        assert active.largest_safe_grid_radius == "5/512"

    if args.json:
        payload: list[dict[str, Any]] = [asdict(gate) for gate in gates]
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_human(gates)
        print("m2_high_agreement_frontier_gate: PASS")


if __name__ == "__main__":
    main()
