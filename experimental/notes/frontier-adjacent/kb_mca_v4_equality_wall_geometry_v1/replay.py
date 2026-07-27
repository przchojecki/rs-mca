#!/usr/bin/env python3
"""Portable replay for the normalized Q=6,u=2 geometry packet."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


if not __debug__:
    raise RuntimeError(
        "Replay refuses optimized execution; rerun without Python -O."
    )


ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent
VERIFY = PACKET / "verification"
EXPERIMENTS = PACKET / "experiments"

VERIFIERS = (
    "verify_regular_grs_mds_deficit_reduction.py",
    "verify_complement_locator_interpolation_descent.py",
    "verify_homogeneous_resultant_factorization.py",
    "verify_minimum_window_coefficient_curve_birationality.py",
    "verify_source_partition_cremona_descent.py",
    "verify_reciprocal_cauchy_separator_target.py",
    "verify_postcritical_reciprocal_cauchy_interpolation.py",
    "search_postcritical_interpolation_counterexamples.py",
    "verify_postcritical_characteristic13_guardrail.py",
    "verify_postcritical_block_line_relation_space.py",
    "verify_cremona_star_hypercohomology_reduction.py",
    "verify_postcritical_diagonal_cauchy_periodicity.py",
    "verify_postcritical_grouped_cauchy_component.py",
    "verify_postcritical_conic_pole_support.py",
    "verify_pole_disjoint_conic_endpoint_target.py",
    "verify_pole_disjoint_conic_facet_collinearity.py",
    "verify_q6_u2_plane_map_reduction.py",
    "verify_q6_u2_normalized_model_search_artifact.py",
)

ORBIT_CLASSIFIER = (
    EXPERIMENTS / "classify_q6_u2_quartic_graph_orbits.py"
)
CPP_SOURCE = EXPERIMENTS / "q6_u2_normalized_model_search.cpp"
FROZEN_CPP_OUTPUT = (
    EXPERIMENTS / "q6_u2_normalized_model_search_output.txt"
)


def run(command: list[str], *, cwd: Path = ROOT) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def check_output(command: list[str], *, cwd: Path = ROOT) -> str:
    print("+", " ".join(command), flush=True)
    completed = subprocess.run(
        command,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.replace("\r\n", "\n").replace("\r", "\n")


def run_python(path: Path, *arguments: str) -> None:
    run([sys.executable, str(path), *arguments])


def replay_certificates(*, tamper: bool) -> None:
    for verifier in VERIFIERS:
        path = VERIFY / verifier
        run_python(path, "--check")
        if tamper:
            run_python(path, "--tamper-selftest")

    orbit_arguments = ["--check"]
    if tamper:
        orbit_arguments.append("--tamper-selftest")
    run_python(ORBIT_CLASSIFIER, *orbit_arguments)


def run_cpp_search() -> None:
    compiler = os.environ.get("CXX") or shutil.which("g++")
    if not compiler:
        raise RuntimeError(
            "Full search replay requires g++ or the CXX environment variable."
        )

    with tempfile.TemporaryDirectory(prefix="kb-q6-u2-") as directory:
        executable = Path(directory) / (
            "q6_u2_normalized_model_search.exe"
            if os.name == "nt"
            else "q6_u2_normalized_model_search"
        )
        run(
            [
                compiler,
                "-O3",
                "-std=c++20",
                str(CPP_SOURCE),
                "-o",
                str(executable),
            ]
        )
        regenerated = check_output([str(executable)])

    frozen = FROZEN_CPP_OUTPUT.read_text(encoding="utf-8")
    frozen = frozen.replace("\r\n", "\n").replace("\r", "\n")
    if regenerated != frozen:
        raise RuntimeError(
            "Regenerated C++ output differs from the frozen artifact."
        )
    print("PASS: compiled C++ search matches frozen output")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--quick", action="store_true")
    mode.add_argument("--full", action="store_true")
    mode.add_argument("--full-search", action="store_true")
    args = parser.parse_args()

    replay_certificates(tamper=args.full or args.full_search)
    if args.full_search:
        run_cpp_search()

    labels = ["exact certificate replay", "compact orbit regeneration"]
    if args.full or args.full_search:
        labels.append("tamper rejection")
    if args.full_search:
        labels.append("compiled C++ search regeneration")
    print("PASS: " + ", ".join(labels))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
