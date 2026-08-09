#!/usr/bin/env python3
"""Locally replay the source-bound cell-5 xi=3 pairings 3-5 census.

The driver reads exact compiler and input artifacts from a checkout of the
public rs-mca-prize-dag repository.  It never imports or calls Modal.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import itertools
import json
import subprocess
import time
from pathlib import Path

import sympy as sp


PRIME = 2_130_706_433
SOURCE_COMMIT = "28b3bc8ab13e94c25088e904251eb5cf49e68ad2"
SOURCE_HASHES = {
    "template_3": "ed1133214b5126f59279ccc75b91f4a572ef9cb62d6b24d8c84df8377da4ce5c",
    "template_4": "0992beedc8d85e1d7e510d40dadccd72d01e8b38325d9e6fe56c741ab50711fd",
    "template_5": "f1dd2096b7dfb7cf6a4a784ae04ef5a0fbd8b6e91f5bfa21bd584d990625f342",
    "tower": "68c18173d4133f66a85136b1ecc33235f7e979c26b6f96d8592030901a8a335c",
    "kernel": "627a8df8bb8a2da4e11488658d1c2145b8c65ef7fbcef3f0f4f53f9d05ea752d",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_paths(dag_root: Path) -> dict[str, Path]:
    directory = dag_root / "experiments/prize_resolution"
    return {
        "template_3": directory / (
            "rate_half_kb_positive_433_1b_cell4_xi3_"
            "pairing3_reciprocal_square_modal.py"
        ),
        "template_4": directory / (
            "rate_half_kb_positive_433_1b_cell4_xi3_"
            "pairing4_nested_signfree_modal.py"
        ),
        "template_5": directory / (
            "rate_half_kb_positive_433_1b_cell4_xi3_"
            "pairing5_nested_signfree_modal.py"
        ),
        "tower": directory / (
            "rate_half_kb_positive_433_1b_cell5_four_basis_tower_result.json"
        ),
        "kernel": directory / (
            "rate_half_kb_positive_433_1b_cell5_compact_kernel_result.json"
        ),
    }


def verify_sources(dag_root: Path, paths: dict[str, Path]) -> None:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=dag_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if head != SOURCE_COMMIT:
        raise RuntimeError(f"source commit mismatch: {head}")
    observed = {name: sha256(path) for name, path in paths.items()}
    if observed != SOURCE_HASHES:
        raise RuntimeError(f"source hash mismatch: {observed}")


def singular_text(expression, variables) -> str:
    terms = []
    for exponents, coefficient in sp.Poly(
        sp.sympify(expression), *variables, modulus=PRIME
    ).terms():
        monomial = str(int(coefficient) % PRIME)
        for variable, exponent in zip(variables, exponents):
            if exponent:
                monomial += str(variable)
                if exponent != 1:
                    monomial += str(exponent)
        terms.append(monomial)
    return "+".join(terms) if terms else "0"


def make_structure(tower: dict, target: Path) -> None:
    t, r, c, b = sp.symbols("t r c b")
    variables = (t, r, c, b)
    rows = []
    for row in tower["rows"]:
        if row["c_row_index"] != 6:
            continue
        lex_basis = [{"expression": "0"} for _ in range(6)]
        lex_basis[0]["expression"] = singular_text(row["base"]["expression"], variables)
        lex_basis[1]["expression"] = singular_text(row["b_relation"]["expression"], variables)
        lex_basis[5]["expression"] = singular_text(row["c_relation"]["expression"], variables)
        rows.append({"epsilon": row["epsilon"], "chart": 0, "lex_basis": lex_basis})
    target.write_text(json.dumps({"rows": rows}))


def load_compiler(template: Path, structure: Path, kernel: Path):
    tree = ast.parse(template.read_text())
    function = next(
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "evaluate_case"
    )
    function.decorator_list = []
    module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
    namespace = {
        "hashlib": hashlib,
        "json": json,
        "Path": Path,
        "time": time,
        "PRIME": PRIME,
        "REMOTE_STRUCTURE": str(structure),
        "REMOTE_KERNEL": str(kernel),
    }
    exec(compile(module, str(template), "exec"), namespace)
    return namespace["evaluate_case"]


def all_cases() -> tuple[tuple[int, ...], ...]:
    signs = tuple(itertools.product((-1, 1), repeat=2))
    return (
        tuple((*epsilon, sigma_c, 3) for epsilon in signs for sigma_c in (-1, 1))
        + tuple((*epsilon, 4) for epsilon in signs)
        + tuple((*epsilon, sigma_c, 5) for epsilon in signs for sigma_c in (-1, 1))
    )


def evaluate_row(case, compilers, tower):
    pairing = case[-1]
    result = compilers[pairing](case[:-1])
    t, r, c, b = sp.symbols("t r c b")
    tower_row = next(
        row
        for row in tower["rows"]
        if row["epsilon"] == list(case[:2]) and row["c_row_index"] == 6
    )
    b_leading = sp.sympify(tower_row["b_leading"]["expression"])
    c_leading = sp.sympify(tower_row["c_leading"]["expression"])
    unresolved = []
    for item in result["unresolved"]:
        substitutions = {
            r: item.get("r", 0),
            t: item.get("t", 0),
            b: item.get("b", 0),
            c: item.get("c", 0),
        }
        if (
            item["reason"] == "FREE_B"
            and int(b_leading.subs(substitutions)) % PRIME == 0
        ):
            result["boundary_rows"].append({**item, "stage": "CELL5_B_LEADING"})
        elif (
            item["reason"] == "FREE_C"
            and int(c_leading.subs(substitutions)) % PRIME == 0
        ):
            result["boundary_rows"].append({**item, "stage": "CELL5_C_LEADING"})
        else:
            unresolved.append(item)
    result["unresolved"] = unresolved
    result["status"] = "COMPLETE" if not unresolved else "INCOMPLETE"
    result["target_excluded"] = not unresolved and result["witness_count"] == 0
    return result


def parse_indices(text: str) -> list[int]:
    if text == "all":
        return list(range(20))
    indices = sorted({int(value) for value in text.split(",") if value})
    if any(index < 0 or index >= 20 for index in indices):
        raise ValueError("indices must lie in 0..19")
    return indices


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dag-root", required=True, type=Path)
    parser.add_argument("--indices", default="all")
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()

    paths = source_paths(arguments.dag_root)
    verify_sources(arguments.dag_root, paths)
    tower = json.loads(paths["tower"].read_text())
    structure = arguments.output.with_suffix(".structure.json")
    make_structure(tower, structure)
    compilers = {
        pairing: load_compiler(paths[f"template_{pairing}"], structure, paths["kernel"])
        for pairing in (3, 4, 5)
    }
    rows = []
    cases = all_cases()
    for index in parse_indices(arguments.indices):
        started = time.perf_counter()
        row = dict(evaluate_row(cases[index], compilers, tower))
        row.pop("timings", None)
        row["local_case_index"] = index
        row["local_elapsed_seconds"] = round(time.perf_counter() - started, 6)
        rows.append(row)
        print(json.dumps({
            "case_index": index,
            "case": cases[index],
            "status": row["status"],
            "target_excluded": row["target_excluded"],
            "witness_count": row["witness_count"],
            "unresolved": row["unresolved"],
        }, sort_keys=True), flush=True)
    structure.unlink()
    payload = {
        "schema": "kb-mca-v4-433-1b-cell5-xi3-pairings345-raw-replay-v1",
        "field": PRIME,
        "source_commit": SOURCE_COMMIT,
        "source_sha256": SOURCE_HASHES,
        "rows": rows,
    }
    arguments.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
