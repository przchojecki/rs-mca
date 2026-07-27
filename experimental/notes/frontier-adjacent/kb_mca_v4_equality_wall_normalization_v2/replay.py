#!/usr/bin/env python3
"""Portable replay for the equality-wall normalization endpoints."""

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
SCRIPTS = ROOT / "experimental" / "scripts"
VERIFIERS = (
    "verify_kb_mca_v4_equality_wall_locator_cylinder_reduction_v1.py",
    "verify_kb_mca_v4_equality_wall_residue_line_partition_reduction_v1.py",
    "verify_kb_mca_v4_equality_wall_fixed_domain_rank16_normalization_v1.py",
    "verify_kb_mca_v4_equality_wall_kernel_kronecker_source_normalization_v1.py",
    "verify_kb_mca_v4_rank_one_split_scroll_source_fiber_reduction_v1.py",
)


def run(command: list[str]) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--quick", action="store_true")
    mode.add_argument("--full", action="store_true")
    args = parser.parse_args()

    for verifier in VERIFIERS:
        run([sys.executable, str(SCRIPTS / verifier), "--check"])

    if args.full:
        for verifier in VERIFIERS:
            run(
                [
                    sys.executable,
                    str(SCRIPTS / verifier),
                    "--tamper-selftest",
                ]
            )

    print(
        "PASS: exact endpoint replay"
        + (" and tamper rejection" if args.full else "")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
