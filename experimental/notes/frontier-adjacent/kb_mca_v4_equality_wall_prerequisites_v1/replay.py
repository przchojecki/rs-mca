#!/usr/bin/env python3
"""Portable replay for the minimal equality-wall prerequisite closure."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


if not __debug__:
    raise RuntimeError(
        "Replay refuses optimized execution; rerun without Python -O."
    )


ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "experimental" / "scripts"
LEAN = (
    ROOT
    / "experimental"
    / "lean"
    / "kb_mca_v4_tangent_deep_owner_adapter"
)

VERIFIERS = (
    "verify_kb_mca_v4_c5_twist_frobenius9208_adapter_v1.py",
    "verify_kb_mca_v4_tangent_deep_owner_adapter_v1.py",
    "verify_kb_mca_v4_tangent_deep_source_rational_adapter_v1.py",
    "verify_kb_mca_v4_tangent_deep_source_rational_c5_adapter_v1.py",
    "verify_kb_mca_v4_active_carrier_incidence_replay_v1.py",
    "verify_kb_mca_v4_active_full_histogram_replay_v1.py",
    "verify_kb_mca_v4_first_gap_source_interpolation_pencil_v1.py",
    "verify_kb_mca_v4_first_gap_complement_locator_linearization_v1.py",
    "verify_kb_mca_v4_first_gap_outlier_basis_residue_transform_v1.py",
    "verify_kb_mca_v4_first_gap_projective_residue_c5_rank_dichotomy_v1.py",
    "verify_kb_mca_v4_first_gap_source_pencil_image_owner_v1.py",
    "verify_kb_mca_v4_post_first_gap_full_histogram_replay_v1.py",
    "verify_kb_mca_v4_next_slack_source_plane_closure_v1.py",
    "verify_kb_mca_v4_post_next_slack_full_histogram_replay_v1.py",
    "verify_kb_mca_v4_successor_upper_stratum_quadratic_adjugate_v1.py",
    "verify_kb_mca_v4_successor_lower_stratum_segre_descent_v1.py",
    "verify_kb_mca_v4_post_successor_full_histogram_replay_v1.py",
    "verify_kb_mca_v4_second_successor_lower_source_plane_v1.py",
    "verify_kb_mca_v4_second_successor_upper_intrinsic_plane_descent_v1.py",
    "verify_kb_mca_v4_post_second_successor_full_histogram_replay_v1.py",
    "verify_kb_mca_v4_reciprocal_kernel_plane_sweep_v1.py",
    "verify_kb_mca_v4_post_reciprocal_kernel_plane_sweep_full_histogram_replay_v1.py",
)


def run(command: list[str], cwd: Path = ROOT) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def lake_command() -> str:
    discovered = shutil.which("lake")
    if discovered:
        return discovered
    elan_home = Path(
        os.environ.get("ELAN_HOME", Path.home() / ".elan")
    )
    candidate = elan_home / "bin" / (
        "lake.exe" if sys.platform == "win32" else "lake"
    )
    if candidate.is_file():
        return str(candidate)
    raise RuntimeError(
        "lake was not found; install elan or set ELAN_HOME to the "
        "toolchain manager directory"
    )


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
        run([lake_command(), "build"], cwd=LEAN)

    print(
        "PASS: exact certificate replay"
        + (", tamper rejection, and Lean build" if args.full else "")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
