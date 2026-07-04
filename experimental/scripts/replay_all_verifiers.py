#!/usr/bin/env python
"""Replay RS-MCA verifier scripts and certificate commands.

This is a local replay harness. Raw logs and generated files stay under the lab
output directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import shlex
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_REPO = Path(__file__).resolve().parents[2]
DEFAULT_OUT = Path(os.environ.get("RSMCA_REPLAY_OUT", Path(tempfile.gettempdir()) / "rsmca-replay"))
DEFAULT_WSL_DISTRO = os.environ.get("RSMCA_WSL_DISTRO", "Ubuntu")
DEFAULT_WSL_SAGE = os.environ.get("RSMCA_WSL_SAGE", "sage")
PYTHON_PAT = re.compile(r"^(?:python3|python|\.venv/bin/python|[A-Za-z_][A-Za-z0-9_]*=.*)?\s*(?:python3|python|\.venv/bin/python)\s+")
SAGE_PAT = re.compile(r"^(?:[A-Za-z_][A-Za-z0-9_]*=.*\s+)?sage(?:\s+-python)?\s+")
SAGE_NATIVE_CASES = {
    "experimental/scripts/audit_m1_interleaved_list_threshold_descent.sage": "threshold-descent",
    "experimental/scripts/audit_m1_interleaved_list_threshold_interval_sharpening.sage": "threshold-interval-sharpening",
    "experimental/scripts/audit_m1_interleaved_list_threshold_upward_push.sage": "threshold-upward-push",
    "experimental/scripts/audit_m1_interleaved_list_hybrid_quotient_residual.sage": "hybrid-quotient-residual",
    (
        "experimental/scripts/locator/sage_locator_fiber_crosscheck/"
        "sage_locator_fiber_crosscheck.sage"
    ): "locator-selected",
}


@dataclass(frozen=True)
class Task:
    task_id: str
    kind: str
    command: list[str]
    source: str
    timeout_s: int
    cwd: str | None = None


@dataclass
class Result:
    task_id: str
    kind: str
    source: str
    command: list[str]
    classification: str
    exit_code: int | None
    runtime_s: float
    stdout_path: str | None
    stderr_path: str | None
    stdout_tail: str
    stderr_tail: str
    note: str = ""


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def task_id_from(parts: Iterable[str]) -> str:
    raw = "__".join(parts)
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", raw).strip("_")
    return cleaned[:180]


def log_stem_for(task_id: str, max_chars: int = 96) -> str:
    if len(task_id) <= max_chars:
        return task_id
    digest = hashlib.sha256(task_id.encode("utf-8")).hexdigest()[:12]
    prefix = task_id[: max_chars - len(digest) - 2].rstrip("._-")
    return f"{prefix}__{digest}"


def windows_to_wsl_path(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    if drive:
        parts = [part for part in resolved.parts[1:]]
        return f"/mnt/{drive}/" + "/".join(parts)
    return resolved.as_posix()


def probe_wsl_sage(*, distro: str, sage_path: str) -> str | None:
    wsl = shutil.which("wsl")
    if wsl is None:
        return None
    try:
        probe = subprocess.run(
            [wsl, "-d", distro, "--exec", sage_path, "-v"],
            text=True,
            capture_output=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    combined = f"{probe.stdout}\n{probe.stderr}"
    if probe.returncode == 0 and "SageMath version" in combined:
        return wsl
    return None


@dataclass(frozen=True)
class SageBackend:
    kind: str
    executable: str | None = None
    wsl_distro: str | None = None
    wsl_sage: str | None = None


def resolve_sage_backend(
    *,
    mode: str,
    wsl_distro: str,
    wsl_sage: str,
) -> SageBackend:
    native_sage = shutil.which("sage")
    if mode in {"auto", "native"} and native_sage is not None:
        return SageBackend(kind="native", executable=native_sage)
    if mode in {"auto", "wsl"}:
        wsl = probe_wsl_sage(distro=wsl_distro, sage_path=wsl_sage)
        if wsl is not None:
            return SageBackend(
                kind="wsl",
                executable=wsl,
                wsl_distro=wsl_distro,
                wsl_sage=wsl_sage,
            )
    return SageBackend(kind="companion")


def discover_script_tasks(repo: Path, python: str, timeout_s: int) -> list[Task]:
    patterns = [
        "experimental/scripts/verify_*.py",
        "experimental/scripts/*_audit.py",
        "experimental/scripts/*_inventory.py",
        "experimental/data/**/verify_*.py",
        "experimental/scripts/codex_f1_l1_20260617/verifiers/verify_*.py",
    ]
    scripts: dict[Path, str] = {}
    for pattern in patterns:
        for path in repo.glob(pattern):
            if path.is_file():
                scripts[path] = pattern
    tasks: list[Task] = []
    for path in sorted(scripts):
        relative = rel(path, repo)
        tasks.append(
            Task(
                task_id=task_id_from(["script", relative]),
                kind="script-default",
                command=[python, relative],
                source=relative,
                timeout_s=timeout_s,
            )
        )
    return tasks


def discover_sage_tasks(
    repo: Path,
    python: str,
    timeout_s: int,
    sage_mode: str,
    wsl_distro: str,
    wsl_sage: str,
) -> list[Task]:
    backend = resolve_sage_backend(
        mode=sage_mode,
        wsl_distro=wsl_distro,
        wsl_sage=wsl_sage,
    )
    tasks: list[Task] = []
    repo_wsl = windows_to_wsl_path(repo)
    for relative, native_case in SAGE_NATIVE_CASES.items():
        script = repo / relative
        if not script.exists():
            continue
        if backend.kind == "native":
            command = [backend.executable or "sage", str(script)]
            if relative.endswith("sage_locator_fiber_crosscheck.sage"):
                command = [
                    backend.executable or "sage",
                    "-python",
                    str(script),
                    "--preset",
                    "selected",
                    "--max-witnesses",
                    "0",
                ]
            source_note = relative
        elif backend.kind == "wsl":
            script_wsl = windows_to_wsl_path(script)
            command = [
                backend.executable or "wsl",
                "-d",
                backend.wsl_distro or wsl_distro,
                "--cd",
                repo_wsl,
                "--exec",
                backend.wsl_sage or wsl_sage,
                script_wsl,
            ]
            if relative.endswith("sage_locator_fiber_crosscheck.sage"):
                command = [
                    backend.executable or "wsl",
                    "-d",
                    backend.wsl_distro or wsl_distro,
                    "--cd",
                    repo_wsl,
                    "--exec",
                    backend.wsl_sage or wsl_sage,
                    "-python",
                    script_wsl,
                    "--preset",
                    "selected",
                    "--max-witnesses",
                    "0",
                ]
            source_note = f"{relative} (WSL Sage: {backend.wsl_distro})"
        else:
            command = [
                python,
                "experimental/scripts/verify_native_sage_replays.py",
                "--case",
                native_case,
            ]
            source_note = f"{relative} (native companion: {native_case})"
        task_timeout = max(timeout_s, 180) if native_case == "threshold-interval-sharpening" else timeout_s
        tasks.append(
            Task(
                task_id=task_id_from(["sage", relative]),
                kind=(
                    "sage-script"
                    if backend.kind == "native"
                    else "sage-wsl-script"
                    if backend.kind == "wsl"
                    else "sage-native-companion"
                ),
                command=command,
                source=source_note,
                timeout_s=task_timeout,
            )
        )
    return tasks


def logical_command_lines(text: str) -> list[str]:
    commands: list[str] = []
    current = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("```") or line in {"bash", "sh"}:
            continue
        if current:
            current += " " + line
        else:
            current = line
        if current.endswith("\\"):
            current = current[:-1].rstrip()
            continue
        commands.append(current)
        current = ""
    if current:
        commands.append(current)
    return commands


def redirect_output_args(parts: list[str], generated_root: Path) -> list[str]:
    redirected = list(parts)
    output_flags = {"--write", "--output", "--json-out", "--md-out"}
    for index, part in enumerate(redirected[:-1]):
        if part not in output_flags:
            continue
        original = Path(redirected[index + 1].strip('"'))
        out_name = original.name or f"{part.lstrip('-')}.out"
        generated_root.mkdir(parents=True, exist_ok=True)
        redirected[index + 1] = str(generated_root / out_name)
    return redirected


def command_from_readme_line(
    line: str,
    repo: Path,
    readme: Path,
    python: str,
    generated_root: Path,
    include_write: bool,
) -> tuple[list[str], str, Path] | None:
    line = line.strip()
    if not line:
        return None
    if SAGE_PAT.match(line):
        return None
    if not PYTHON_PAT.match(line):
        return None
    # Ignore shell assignments and env-var examples for the first portable pass.
    if "$" in line or line.startswith(".venv/"):
        return None
    line = PYTHON_PAT.sub("", line, count=1)
    try:
        parts = shlex.split(line, posix=False)
    except ValueError:
        return None
    if not parts:
        return None
    script = parts[0].strip('"')
    if not script.endswith(".py"):
        return None
    writes_repo_artifact = any(flag in parts for flag in ("--write", "--output", "--json-out", "--md-out"))
    if "--write" in parts and not include_write:
        return None
    if writes_repo_artifact:
        parts = redirect_output_args(parts, generated_root)
    cwd = repo
    if not (repo / script).exists() and (readme.parent / script).exists():
        cwd = readme.parent
    command = [python, script, *[part.strip('"') for part in parts[1:]]]
    return command, script, cwd


def discover_readme_tasks(
    repo: Path,
    python: str,
    generated_root: Path,
    timeout_s: int,
    include_write: bool,
) -> list[Task]:
    tasks: list[Task] = []
    for readme in sorted(repo.glob("experimental/**/README.md")) + sorted(
        repo.glob("scripts/**/README.md")
    ):
        text = readme.read_text(encoding="utf-8", errors="replace")
        for index, line in enumerate(logical_command_lines(text), start=1):
            parsed = command_from_readme_line(
                line,
                repo,
                readme,
                python,
                generated_root / task_id_from([rel(readme, repo), str(index)]),
                include_write,
            )
            if parsed is None:
                continue
            command, script, cwd = parsed
            tasks.append(
                Task(
                    task_id=task_id_from(["readme", rel(readme, repo), str(index), script]),
                    kind="readme-command",
                    command=command,
                    source=f"{rel(readme, repo)}:{index}",
                    timeout_s=timeout_s,
                    cwd=str(cwd),
                )
            )
    return tasks


def discover_certificate_scanner_tasks(repo: Path, python: str, out: Path, timeout_s: int) -> list[Task]:
    scanner = repo / "experimental/notes/certificate_scanner/certificate_scanner.py"
    examples = sorted((repo / "experimental/notes/certificate_scanner/examples").glob("*.json"))
    tasks: list[Task] = []
    for example in examples:
        stem = example.stem
        generated = out / "certificate_scanner" / stem
        generated.parent.mkdir(parents=True, exist_ok=True)
        tasks.append(
            Task(
                task_id=task_id_from(["certificate_scanner", stem]),
                kind="certificate-scanner",
                command=[
                    python,
                    rel(scanner, repo),
                    rel(example, repo),
                    "--json-out",
                    str(generated.with_suffix(".report.json")),
                    "--md-out",
                    str(generated.with_suffix(".report.md")),
                    "--pretty",
                ],
                source=rel(example, repo),
                timeout_s=timeout_s,
            )
        )
    return tasks


def discover_aperiodic_packet_tasks(repo: Path, python: str, timeout_s: int) -> list[Task]:
    checker = repo / "scripts/check_aperiodic_eliminant_packet.py"
    tasks: list[Task] = []
    for packet in sorted(repo.glob("experimental/data/certificates/**/*.json")):
        try:
            text = packet.read_text(encoding="utf-8", errors="replace")
            if '"schema_version"' not in text or "aperiodic-hankel-eliminant-v1" not in text:
                continue
        except OSError:
            continue
        command = [python, rel(checker, repo), rel(packet, repo)]
        if "invalid" in packet.name:
            command.insert(2, "--expect-fail")
        tasks.append(
            Task(
                task_id=task_id_from(["aperiodic_packet", rel(packet, repo)]),
                kind="aperiodic-packet",
                command=command,
                source=rel(packet, repo),
                timeout_s=timeout_s,
            )
        )
    return tasks


def unique_tasks(tasks: list[Task]) -> list[Task]:
    seen: set[tuple[str, ...]] = set()
    out: list[Task] = []
    for task in tasks:
        key = (task.cwd or "", *task.command)
        if key in seen:
            continue
        seen.add(key)
        out.append(task)
    return out


def classify(exit_code: int | None, stdout: str, stderr: str, timed_out: bool) -> tuple[str, str]:
    combined = f"{stdout}\n{stderr}".lower()
    if timed_out:
        return "TIMEOUT", "process exceeded timeout"
    if exit_code == 0:
        if re.search(r"(?im)^\s*(?:replay_classification|replay_result)\s*:\s*skip(?:-external)?\s*$", combined):
            return "SKIP-external", "script emitted explicit replay skip sentinel"
        return "PASS", ""
    if exit_code == 2 and ("usage:" in combined or "required" in combined):
        return "SKIP-needs-args", "argparse usage/required argument"
    if "modulenotfounderror" in combined or "importerror" in combined:
        return "FAIL-missing-import", "missing Python dependency"
    if "no such file" in combined or "filenotfounderror" in combined:
        return "FAIL-path", "missing file/path"
    return "FAIL", ""


def tail(text: str, max_chars: int = 1800) -> str:
    text = text.replace("\r\n", "\n")
    if len(text) <= max_chars:
        return text
    return text[-max_chars:]


def run_task(task: Task, repo: Path, logs: Path, env: dict[str, str]) -> Result:
    logs.mkdir(parents=True, exist_ok=True)
    log_stem = log_stem_for(task.task_id)
    stdout_path = logs / f"{log_stem}.stdout.txt"
    stderr_path = logs / f"{log_stem}.stderr.txt"
    start = time.perf_counter()
    timed_out = False
    try:
        proc = subprocess.run(
            task.command,
            cwd=Path(task.cwd) if task.cwd else repo,
            env=env,
            text=True,
            capture_output=True,
            timeout=task.timeout_s,
        )
        stdout = proc.stdout
        stderr = proc.stderr
        exit_code: int | None = proc.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        exit_code = None
    runtime_s = time.perf_counter() - start
    stdout_path.write_text(stdout, encoding="utf-8", errors="replace")
    stderr_path.write_text(stderr, encoding="utf-8", errors="replace")
    classification, note = classify(exit_code, stdout, stderr, timed_out)
    return Result(
        task_id=task.task_id,
        kind=task.kind,
        source=task.source,
        command=task.command,
        classification=classification,
        exit_code=exit_code,
        runtime_s=round(runtime_s, 3),
        stdout_path=str(stdout_path),
        stderr_path=str(stderr_path),
        stdout_tail=tail(stdout),
        stderr_tail=tail(stderr),
        note=note,
    )


def format_markdown(results: list[Result], metadata: dict[str, object]) -> str:
    counts: dict[str, int] = {}
    for result in results:
        counts[result.classification] = counts.get(result.classification, 0) + 1
    lines = [
        "# RS-MCA Verification Replay Matrix",
        "",
        "Status: AUDIT / local replay.",
        "",
        "## Metadata",
        "",
    ]
    for key, value in metadata.items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Summary", ""])
    for key in sorted(counts):
        lines.append(f"- `{key}`: {counts[key]}")
    lines.extend(["", "## Results", ""])
    lines.append("| Classification | Runtime s | Source | Command | Note |")
    lines.append("|---|---:|---|---|---|")
    for result in results:
        cmd = " ".join(result.command).replace("|", "\\|")
        note = result.note.replace("|", "\\|")
        lines.append(
            f"| `{result.classification}` | {result.runtime_s:.3f} | `{result.source}` | `{cmd}` | {note} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--include-write", action="store_true")
    parser.add_argument("--only", choices=("all", "scripts", "readmes", "scanner", "packets", "sage"), default="all")
    parser.add_argument(
        "--sage-mode",
        choices=("auto", "native", "wsl", "companion"),
        default="auto",
        help="Sage replay backend: native PATH sage, WSL Sage, or native Python companions",
    )
    parser.add_argument("--wsl-distro", default=DEFAULT_WSL_DISTRO)
    parser.add_argument("--wsl-sage", default=DEFAULT_WSL_SAGE)
    args = parser.parse_args()

    repo = args.repo.resolve()
    out = args.out.resolve()
    generated = out / "generated"
    logs = out / "logs"
    out.mkdir(parents=True, exist_ok=True)
    generated.mkdir(parents=True, exist_ok=True)

    tasks: list[Task] = []
    if args.only in {"all", "scripts"}:
        tasks.extend(discover_script_tasks(repo, args.python, args.timeout))
    if args.only in {"all", "sage"}:
        tasks.extend(
            discover_sage_tasks(
                repo,
                args.python,
                args.timeout,
                args.sage_mode,
                args.wsl_distro,
                args.wsl_sage,
            )
        )
    if args.only in {"all", "readmes"}:
        tasks.extend(discover_readme_tasks(repo, args.python, generated, args.timeout, args.include_write))
    if args.only in {"all", "scanner"}:
        tasks.extend(discover_certificate_scanner_tasks(repo, args.python, out, args.timeout))
    if args.only in {"all", "packets"}:
        tasks.extend(discover_aperiodic_packet_tasks(repo, args.python, args.timeout))
    tasks = unique_tasks(tasks)
    if args.limit:
        tasks = tasks[: args.limit]

    env = os.environ.copy()
    # Keep repo imports stable for scripts that import sibling experimental modules.
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = os.pathsep.join(
        part for part in [str(repo), str(repo / "experimental/scripts"), existing_pythonpath] if part
    )

    results = [run_task(task, repo, logs, env) for task in tasks]
    metadata = {
        "repo": str(repo),
        "out": str(out),
        "python": args.python,
        "timeout": args.timeout,
        "task_count": len(tasks),
        "include_write": args.include_write,
        "only": args.only,
        "sage_mode": args.sage_mode,
        "wsl_distro": args.wsl_distro,
        "wsl_sage": args.wsl_sage,
        "cwd_policy": "repo root unless a README command script is local to its README directory",
        "output_policy": "README --write/--output/--json-out/--md-out targets are redirected under the lab output directory",
    }
    matrix = {"metadata": metadata, "results": [asdict(result) for result in results]}
    (out / "matrix.json").write_text(json.dumps(matrix, indent=2), encoding="utf-8")
    (out / "matrix.md").write_text(format_markdown(results, metadata), encoding="utf-8")
    print(format_markdown(results, metadata), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
