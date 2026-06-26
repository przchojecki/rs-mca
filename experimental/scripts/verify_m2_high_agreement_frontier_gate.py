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
    exact_start: int
    budget: int
    exact_start_count: int
    status: str
    last_unsafe_agreement: int | None
    first_safe_agreement: int | None
    last_unsafe_distance: int | None
    first_safe_distance: int | None
    unsafe_radius: str | None
    safe_radius: str | None


def ceil_div(num: int, den: int) -> int:
    return -(-num // den)


def tangent_gate(label: str, n: int, k: int, q_line: int, eps_bits: int) -> Gate:
    if not (0 <= k < n):
        raise ValueError("expected 0 <= k < n")
    if q_line <= 0:
        raise ValueError("expected positive q_line")
    if eps_bits < 0:
        raise ValueError("expected nonnegative eps_bits")

    exact_start = ceil_div(2 * n + k, 3)
    assert k + 1 <= exact_start <= n
    exact_start_count = n - exact_start + 1
    budget = q_line // (1 << eps_bits)

    if budget == 0:
        status = "no_safe_agreement_in_exact_tangent_range"
        return Gate(
            label=label,
            n=n,
            k=k,
            q_line=q_line,
            eps_bits=eps_bits,
            exact_start=exact_start,
            budget=budget,
            exact_start_count=exact_start_count,
            status=status,
            last_unsafe_agreement=n,
            first_safe_agreement=None,
            last_unsafe_distance=0,
            first_safe_distance=None,
            unsafe_radius="0",
            safe_radius=None,
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
            exact_start=exact_start,
            budget=budget,
            exact_start_count=exact_start_count,
            status="crossing_inside_exact_tangent_range",
            last_unsafe_agreement=last_unsafe,
            first_safe_agreement=first_safe,
            last_unsafe_distance=n - last_unsafe,
            first_safe_distance=n - first_safe,
            unsafe_radius=str(Fraction(n - last_unsafe, n)),
            safe_radius=str(Fraction(n - first_safe, n)),
        )

    return Gate(
        label=label,
        n=n,
        k=k,
        q_line=q_line,
        eps_bits=eps_bits,
        exact_start=exact_start,
        budget=budget,
        exact_start_count=exact_start_count,
        status="exact_tangent_range_already_within_budget",
        last_unsafe_agreement=None,
        first_safe_agreement=exact_start,
        last_unsafe_distance=None,
        first_safe_distance=n - exact_start,
        unsafe_radius=None,
        safe_radius=str(Fraction(n - exact_start, n)),
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
    assert gate.exact_start == ceil_div(2 * gate.n + gate.k, 3)
    assert gate.exact_start_count == gate.n - gate.exact_start + 1
    assert gate.budget == gate.q_line // (1 << gate.eps_bits)

    if gate.status == "crossing_inside_exact_tangent_range":
        assert gate.last_unsafe_agreement is not None
        assert gate.first_safe_agreement is not None
        assert gate.last_unsafe_agreement + 1 == gate.first_safe_agreement
        assert gate.last_unsafe_agreement >= gate.exact_start
        assert gate.n - gate.last_unsafe_agreement + 1 == gate.budget + 1
        assert gate.n - gate.first_safe_agreement + 1 == gate.budget
        assert (gate.budget + 1) * (1 << gate.eps_bits) > gate.q_line
        assert gate.budget * (1 << gate.eps_bits) <= gate.q_line
    elif gate.status == "exact_tangent_range_already_within_budget":
        assert gate.budget >= gate.exact_start_count
        assert gate.first_safe_agreement == gate.exact_start
    elif gate.status == "no_safe_agreement_in_exact_tangent_range":
        assert gate.budget == 0
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
            label="toy exact range already safe",
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
        print(f"  exact_start={gate.exact_start}")
        print(f"  exact_start_count={gate.exact_start_count}")
        print(f"  budget=floor(q_line/2^eps_bits)={gate.budget}")
        print(f"  status={gate.status}")
        if gate.last_unsafe_agreement is not None:
            print(
                "  last_unsafe_agreement="
                f"{gate.last_unsafe_agreement}, distance={gate.last_unsafe_distance}, "
                f"radius={gate.unsafe_radius}"
            )
        if gate.first_safe_agreement is not None:
            print(
                "  first_safe_agreement="
                f"{gate.first_safe_agreement}, distance={gate.first_safe_distance}, "
                f"radius={gate.safe_radius}"
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
        assert active.budget == 6
        assert active.status == "crossing_inside_exact_tangent_range"
        assert active.last_unsafe_agreement == 506
        assert active.first_safe_agreement == 507
        assert active.last_unsafe_distance == 6
        assert active.first_safe_distance == 5
        assert active.unsafe_radius == "3/256"
        assert active.safe_radius == "5/512"

    if args.json:
        payload: list[dict[str, Any]] = [asdict(gate) for gate in gates]
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_human(gates)
        print("m2_high_agreement_frontier_gate: PASS")


if __name__ == "__main__":
    main()
