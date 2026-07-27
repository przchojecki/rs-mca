#!/usr/bin/env python3
"""Portable replay for the Q=6, u=2 P3+C3 exclusion packet."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


if not __debug__:
    raise RuntimeError(
        "Replay refuses optimized execution; rerun without Python -O."
    )


ROOT = Path(__file__).resolve().parents[4]
GEOMETRY = (
    ROOT
    / "experimental"
    / "notes"
    / "frontier-adjacent"
    / "kb_mca_v4_equality_wall_geometry_v1"
)

PROGRAMS = [
    GEOMETRY / "experiments" / "classify_q6_u2_conic_graph_orbits.py",
    GEOMETRY / "experiments" / "generate_q6_u2_conic_decic_gates.py",
    GEOMETRY
    / "verification"
    / "verify_q6_u2_line_conic_quotient_reduction.py",
    GEOMETRY / "verification" / "verify_q6_u2_star_conic_geometry.py",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def run(program: Path, argument: str) -> None:
    require(program.is_file(), f"missing replay program: {program}")
    command = [sys.executable, str(program), argument]
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--quick", action="store_true")
    mode.add_argument("--full", action="store_true")
    args = parser.parse_args()

    for program in PROGRAMS:
        run(program, "--check")

    if args.full:
        for program in PROGRAMS:
            run(program, "--tamper-selftest")

    print(
        "P3+C3 packet replay: PASS "
        f"mode={'full' if args.full else 'quick'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
