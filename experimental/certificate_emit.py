#!/usr/bin/env python3
"""Emit a small Markdown or TeX certificate from JSON script output.

The expected JSON shape follows the script-output standard in agents.md:
input parameters, mathematical object, result, proof certificate or
reproducibility data, theorem/problem support, and proof status.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SECTION_KEYS = (
    ("input_parameters", "Input Parameters"),
    ("mathematical_object", "Mathematical Object"),
    ("result", "Result"),
    ("proof_certificate", "Proof Certificate"),
)

META_KEYS = (
    ("status", "Status"),
    ("theorem_or_problem", "Theorem/problem"),
    ("source", "Source"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="JSON certificate input")
    parser.add_argument(
        "--format",
        choices=("markdown", "tex"),
        default="markdown",
        help="output format",
    )
    parser.add_argument("--output", type=Path, help="write output to this path")
    parser.add_argument("--title", help="override the certificate title")
    return parser.parse_args()


def load_certificates(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        return data
    raise ValueError("input JSON must be an object or a list of objects")


def compact_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(", ", ": "))


def compact_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value
    return compact_json(value)


def flatten_items(value: Any, prefix: str = "") -> list[tuple[str, str]]:
    if not isinstance(value, dict):
        return [(prefix or "value", compact_value(value))]

    rows: list[tuple[str, str]] = []
    for key in sorted(value):
        next_key = f"{prefix}.{key}" if prefix else str(key)
        item = value[key]
        if isinstance(item, dict):
            rows.extend(flatten_items(item, next_key))
        else:
            rows.append((next_key, compact_value(item)))
    return rows


def markdown_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("|", "\\|")


def tex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def certificate_title(cert: dict[str, Any], fallback: str, override: str | None) -> str:
    if override is not None:
        return override
    title = cert.get("title")
    if isinstance(title, str) and title.strip():
        return title
    return fallback


def emit_markdown_table(rows: list[tuple[str, str]]) -> list[str]:
    if not rows:
        return ["_No entries._"]
    lines = ["| Key | Value |", "| --- | --- |"]
    for key, value in rows:
        lines.append(f"| `{markdown_escape(key)}` | {markdown_escape(value)} |")
    return lines


def emit_markdown(cert: dict[str, Any], title: str) -> str:
    lines = [f"# {title}", ""]
    for key, label in META_KEYS:
        if key in cert:
            lines.append(f"- **{label}:** {compact_value(cert[key])}")
    lines.append("")

    for key, label in SECTION_KEYS:
        lines.append(f"## {label}")
        lines.append("")
        lines.extend(emit_markdown_table(flatten_items(cert.get(key, {}))))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def emit_tex_table(rows: list[tuple[str, str]]) -> list[str]:
    if not rows:
        return [r"\emph{No entries.}"]
    lines = [r"\begin{tabular}{p{0.32\linewidth}p{0.60\linewidth}}", r"\toprule"]
    lines.append(r"Key & Value \\")
    lines.append(r"\midrule")
    for key, value in rows:
        lines.append(f"{tex_escape(key)} & {tex_escape(value)} \\\\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    return lines


def emit_tex(cert: dict[str, Any], title: str) -> str:
    lines = [rf"\paragraph{{{tex_escape(title)}}}", r"\begin{description}"]
    for key, label in META_KEYS:
        if key in cert:
            lines.append(rf"\item[{tex_escape(label)}] {tex_escape(compact_value(cert[key]))}")
    lines.append(r"\end{description}")
    lines.append("")

    for key, label in SECTION_KEYS:
        lines.append(rf"\subparagraph{{{tex_escape(label)}}}")
        lines.extend(emit_tex_table(flatten_items(cert.get(key, {}))))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render(
    certificates: list[dict[str, Any]],
    input_path: Path,
    fmt: str,
    title: str | None,
) -> str:
    rendered = []
    multi = len(certificates) > 1
    for index, cert in enumerate(certificates, start=1):
        fallback = input_path.stem if not multi else f"{input_path.stem} {index}"
        cert_title = certificate_title(cert, fallback, title if not multi else None)
        if fmt == "markdown":
            rendered.append(emit_markdown(cert, cert_title))
        else:
            rendered.append(emit_tex(cert, cert_title))
    return "\n".join(part.rstrip() for part in rendered) + "\n"


def main() -> int:
    args = parse_args()
    certificates = load_certificates(args.input)
    output = render(certificates, args.input, args.format, args.title)
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
