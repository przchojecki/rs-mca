#!/usr/bin/env python3
"""Build a local EXPERIMENTAL locator-fiber evidence packet."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable


REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.locator.locator_fiber_crosscheck_report.compare_locator_fiber_outputs import (
    CLAIM as COMPARISON_CLAIM,
)
from experimental.scripts.locator.locator_fiber_crosscheck_report.compare_locator_fiber_outputs import (
    compare_files,
)
from experimental.scripts.locator.locator_fiber_sweep.run_locator_fiber_sweep import (
    CLAIM as SWEEP_CLAIM,
)
from experimental.scripts.locator.locator_fiber_sweep.run_locator_fiber_sweep import (
    DEFAULT_MAX_SUPPORTS,
    STATUS,
    SweepCase,
    build_markdown as build_sweep_markdown,
    current_repo_commit,
    output_name,
    run_case,
    utc_now,
    write_csv,
)


CLAIM = (
    "experimental locator-fiber local packet only; "
    "no RS/list-decoding/MCA safety assertion; "
    "no theorem status upgrade"
)
SAGE_SCRIPT = (
    Path("experimental")
    / "scripts"
    / "locator"
    / "sage_locator_fiber_crosscheck"
    / "sage_locator_fiber_crosscheck.sage"
)
CASE_SETS = ("tiny", "selected")


@dataclass(frozen=True)
class CommandRecord:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str


CommandRunner = Callable[..., subprocess.CompletedProcess[str]]


def repo_root() -> Path:
    return REPO_ROOT


def packet_cases(case_set: str) -> list[SweepCase]:
    if case_set not in CASE_SETS:
        raise ValueError(f"case_set must be one of {', '.join(CASE_SETS)}")
    cases = [
        SweepCase(p=5, n=4, k=2, agreement_size=3, template="monomial", seed=None),
        SweepCase(p=5, n=4, k=2, agreement_size=3, template="zero", seed=None),
    ]
    if case_set == "selected":
        cases.append(
            SweepCase(
                p=17,
                n=16,
                k=8,
                agreement_size=9,
                template="monomial",
                seed=None,
            )
        )
    return cases


def write_json(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def python_sweep_summary(
    *,
    out_dir: Path,
    cases: list[SweepCase],
    max_witnesses: int,
    max_supports: int,
    parameters: dict[str, str],
) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for case in cases:
        report = run_case(
            case,
            out_dir,
            max_witnesses=max_witnesses,
            max_supports=max_supports,
            parameters=parameters,
        )
        rows.append(report)
    rows.sort(
        key=lambda row: (
            row["p"],
            row["k"],
            row["agreement_size"],
            row["template"],
            "null" if row["seed"] is None else str(row["seed"]),
        )
    )
    summary = {
        "schema_version": "locator-fiber-sweep-0.1.0",
        "status": STATUS,
        "claim": SWEEP_CLAIM,
        "output_directory": str(out_dir),
        "rows": rows,
        "provenance": {
            "generator": (
                "experimental/scripts/locator/locator_fiber_sweep/"
                "run_locator_fiber_sweep.py"
            ),
            "repo_commit": current_repo_commit(),
            "created_at_utc": utc_now(),
            "parameters": parameters,
        },
    }
    write_csv(rows, out_dir / "locator_fiber_sweep.csv")
    (out_dir / "locator_fiber_sweep.md").write_text(build_sweep_markdown(summary))
    return summary


def sage_json_name(case: SweepCase) -> str:
    return output_name(case).replace("locator_fiber_", "sage_locator_fiber_")


def sage_command(
    *,
    sage_command_name: str,
    case: SweepCase,
    max_witnesses: int,
    json_out: Path,
) -> list[str]:
    command = [
        sage_command_name,
        "-python",
        str(SAGE_SCRIPT),
        "--p",
        str(case.p),
        "--n",
        str(case.n),
        "--k",
        str(case.k),
        "--agreement-size",
        str(case.agreement_size),
        "--template",
        case.template,
        "--seed",
        str(0 if case.seed is None else case.seed),
        "--max-witnesses",
        str(max_witnesses),
        "--json-out",
        str(json_out),
    ]
    return command


def run_command(
    command: list[str],
    *,
    command_runner: CommandRunner = subprocess.run,
) -> CommandRecord:
    try:
        completed = command_runner(
            command,
            cwd=repo_root(),
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            f"command not found: {command[0]!r}; install Sage or use --sage-command"
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "command failed: "
            f"{' '.join(command)}\nstdout:\n{exc.stdout}\nstderr:\n{exc.stderr}"
        ) from exc
    return CommandRecord(
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def run_sage_crosschecks(
    *,
    out_dir: Path,
    cases: list[SweepCase],
    sage_command_name: str,
    max_witnesses: int,
    command_runner: CommandRunner = subprocess.run,
) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    reports: list[dict[str, Any]] = []
    commands: list[dict[str, Any]] = []
    for case in cases:
        json_path = out_dir / sage_json_name(case)
        command = sage_command(
            sage_command_name=sage_command_name,
            case=case,
            max_witnesses=max_witnesses,
            json_out=json_path,
        )
        record = run_command(command, command_runner=command_runner)
        commands.append(
            {
                "command": record.command,
                "returncode": record.returncode,
                "stdout": record.stdout,
                "stderr": record.stderr,
                "json_file": str(json_path),
            }
        )
        reports.append(json.loads(json_path.read_text()))

    aggregate = {
        "schema_version": "sage-locator-fiber-crosscheck-0.1.0",
        "status": STATUS,
        "claim": (
            "optional Sage finite-field locator-fiber cross-check only; "
            "no RS/list-decoding/MCA safety assertion; "
            "no theorem status upgrade"
        ),
        "reports": reports,
        "provenance": {
            "generator": (
                "experimental/scripts/locator/locator_fiber_local_packet/"
                "run_locator_fiber_local_packet.py"
            ),
            "repo_commit": current_repo_commit(),
            "created_at_utc": utc_now(),
        },
    }
    aggregate_path = out_dir / "sage_locator_fiber_packet.json"
    write_json(aggregate, aggregate_path)
    return {
        "aggregate_json": str(aggregate_path),
        "case_json_files": [item["json_file"] for item in commands],
        "commands": commands,
    }


def check_comparison_summary(summary: dict[str, Any]) -> None:
    if summary["mismatched_cases"]:
        raise RuntimeError("comparison has mismatched Python/Sage cases")
    if summary["python_only_cases"] or summary["sage_only_cases"]:
        raise RuntimeError("comparison has unmatched Python/Sage cases")


def build_packet_markdown(manifest: dict[str, Any]) -> str:
    comparison = manifest["comparison"]["summary"]
    lines = [
        "# Locator-Fiber Local Packet",
        "",
        "Experimental local evidence packet only.",
        "No RS/list-decoding/MCA safety assertion.",
        "No theorem status upgrade.",
        "",
        "## Outputs",
        "",
        "- `python_sweep/locator_fiber_sweep.csv`",
        "- `sage_crosscheck/sage_locator_fiber_packet.json`",
        "- `comparison/locator_fiber_crosscheck_report.json`",
        "- `comparison/locator_fiber_crosscheck_report.md`",
        "",
        "## Comparison Summary",
        "",
        f"- Matched cases: {comparison['matched_cases']}",
        f"- Mismatched cases: {comparison['mismatched_cases']}",
        f"- Python-only cases: {comparison['python_only_cases']}",
        f"- Sage-only cases: {comparison['sage_only_cases']}",
        f"- All matched cases agree: {comparison['all_matched_cases_agree']}",
        "",
        "## Provenance",
        "",
        f"- Status: {manifest['status']}",
        f"- Claim discipline: {manifest['claim']}",
        f"- Case set: {manifest['case_set']}",
        f"- Repo commit: {manifest['provenance']['repo_commit']}",
        f"- Created at UTC: {manifest['provenance']['created_at_utc']}",
        "",
    ]
    return "\n".join(lines)


def parse_parameter(values: Iterable[str]) -> dict[str, str]:
    parameters: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"parameter must be key=value: {value!r}")
        key, item = value.split("=", 1)
        if not key:
            raise ValueError("parameter key must be nonempty")
        parameters[key] = item
    return parameters


def run_packet(
    *,
    out_dir: Path,
    case_set: str = "selected",
    sage_command_name: str = "sage",
    max_witnesses: int = 0,
    max_supports: int = DEFAULT_MAX_SUPPORTS,
    parameters: dict[str, str] | None = None,
    command_runner: CommandRunner = subprocess.run,
    allow_differences: bool = False,
) -> dict[str, Any]:
    if max_witnesses < 0:
        raise ValueError("max_witnesses must be nonnegative")
    if max_supports <= 0:
        raise ValueError("max_supports must be positive")
    parameters = parameters or {}
    cases = packet_cases(case_set)
    out_dir.mkdir(parents=True, exist_ok=True)
    python_dir = out_dir / "python_sweep"
    sage_dir = out_dir / "sage_crosscheck"
    comparison_dir = out_dir / "comparison"

    sweep = python_sweep_summary(
        out_dir=python_dir,
        cases=cases,
        max_witnesses=max_witnesses,
        max_supports=max_supports,
        parameters=parameters,
    )
    sage = run_sage_crosschecks(
        out_dir=sage_dir,
        cases=cases,
        sage_command_name=sage_command_name,
        max_witnesses=max_witnesses,
        command_runner=command_runner,
    )
    comparison = compare_files(
        python_csv=python_dir / "locator_fiber_sweep.csv",
        sage_jsons=[Path(sage["aggregate_json"])],
        out_dir=comparison_dir,
    )
    if not allow_differences:
        check_comparison_summary(comparison["summary"])

    manifest = {
        "schema_version": "locator-fiber-local-packet-0.1.0",
        "status": STATUS,
        "claim": CLAIM,
        "case_set": case_set,
        "output_directory": str(out_dir),
        "python_sweep": {
            "claim": SWEEP_CLAIM,
            "rows": len(sweep["rows"]),
            "csv": str(python_dir / "locator_fiber_sweep.csv"),
        },
        "sage_crosscheck": sage,
        "comparison": {
            "claim": COMPARISON_CLAIM,
            "summary": comparison["summary"],
            "json": str(comparison_dir / "locator_fiber_crosscheck_report.json"),
            "markdown": str(comparison_dir / "locator_fiber_crosscheck_report.md"),
        },
        "provenance": {
            "generator": (
                "experimental/scripts/locator/locator_fiber_local_packet/"
                "run_locator_fiber_local_packet.py"
            ),
            "repo_commit": current_repo_commit(),
            "created_at_utc": utc_now(),
            "parameters": parameters,
        },
    }
    write_json(manifest, out_dir / "packet_manifest.json")
    (out_dir / "packet.md").write_text(build_packet_markdown(manifest))
    return manifest


def format_summary(manifest: dict[str, Any]) -> str:
    summary = manifest["comparison"]["summary"]
    return "\n".join(
        [
            f"Locator-fiber local packet ({manifest['status']})",
            f"case_set={manifest['case_set']}",
            f"output_directory={manifest['output_directory']}",
            f"python_rows={manifest['python_sweep']['rows']}",
            f"matched_cases={summary['matched_cases']}",
            f"mismatched_cases={summary['mismatched_cases']}",
            f"python_only_cases={summary['python_only_cases']}",
            f"sage_only_cases={summary['sage_only_cases']}",
            f"all_matched_cases_agree={summary['all_matched_cases_agree']}",
            f"claim: {manifest['claim']}",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build an EXPERIMENTAL locator-fiber local evidence packet."
    )
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--case-set", choices=CASE_SETS, default="selected")
    parser.add_argument("--sage-command", default="sage")
    parser.add_argument("--max-witnesses", type=int, default=0)
    parser.add_argument("--max-supports", type=int, default=DEFAULT_MAX_SUPPORTS)
    parser.add_argument(
        "--allow-differences",
        action="store_true",
        help="write reports even if Python/Sage comparison is not strict-clean",
    )
    parser.add_argument(
        "--parameter",
        action="append",
        default=[],
        help="Additional provenance parameter as key=value. May be repeated.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        manifest = run_packet(
            out_dir=args.out_dir,
            case_set=args.case_set,
            sage_command_name=args.sage_command,
            max_witnesses=args.max_witnesses,
            max_supports=args.max_supports,
            parameters=parse_parameter(args.parameter),
            allow_differences=args.allow_differences,
        )
    except (RuntimeError, ValueError) as exc:
        parser.error(str(exc))
    print(format_summary(manifest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
