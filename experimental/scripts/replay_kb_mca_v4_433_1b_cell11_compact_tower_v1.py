#!/usr/bin/env python3
"""Replay the guarded compact tower and coefficient kernel for 433-1b cell 11."""

from __future__ import annotations

import argparse
import functools
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path

import sympy as sp


PRIME = 2_130_706_433
CELL = 11
PIVOT = 1
EPSILON = (-1, -1)
SOURCE_COMMIT = "28b3bc8ab13e94c25088e904251eb5cf49e68ad2"
SOURCE_HASHES = {
    "common": "a956656cba6c884bae665a2439666964ed468dcf9d0466e80cb825e811a6f845",
    "product": "ee4dcb25877e9101a544ee5896b9bf6890059d6398c78d7562127b0d1c53c293",
    "pilot": "1590721003b1b8c9f850064eddab82d2fa25ddb93a00ef9d71feaa4d492f16ea",
}
GUARD = "*".join((
    "b", "c", "r", "t", "(b-1)", "(b+1)", "(c-1)", "(c+1)",
    "(b-c)", "(b+c)", "(r^2-1)", "(r^2+1)", "(t^2-1)",
    "(t^2+1)", "(t^2-r^2)", "(t^2+r^2)",
))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_paths(root: Path) -> dict[str, Path]:
    directory = root / "experiments/prize_resolution"
    return {
        "common": directory / "rate_half_kb_positive_433_1b_common_vieta_compiler.py",
        "product": directory / "rate_half_kb_positive_433_1b_product_base_rank_compiler_result.json",
        "pilot": directory / "rate_half_kb_positive_433_1b_cells5_11_pivot_pilot_result.json",
    }


def verify_sources(root: Path, paths: dict[str, Path]) -> None:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    if head != SOURCE_COMMIT:
        raise RuntimeError(f"source commit mismatch: {head}")
    observed = {name: sha256(path) for name, path in paths.items()}
    if observed != SOURCE_HASHES:
        raise RuntimeError(f"source hash mismatch: {observed}")


def parse_singular(text: str, variables: tuple[sp.Symbol, ...]) -> sp.Poly:
    symbols = {str(value): value for value in variables}
    expression = 0
    for term in re.findall(r"[+-]?[^+-]+", text):
        sign = -1 if term.startswith("-") else 1
        unsigned = term.lstrip("+-")
        digits = re.match(r"\d*", unsigned).group()
        monomial = sp.Integer(sign * int(digits or "1"))
        suffix = unsigned[len(digits):]
        cursor = 0
        for match in re.finditer(r"([zcbtr])(\d*)", suffix):
            if match.start() != cursor:
                raise ValueError(f"cannot parse Singular term: {term}")
            variable, exponent = match.groups()
            monomial *= symbols[variable] ** int(exponent or "1")
            cursor = match.end()
        if cursor != len(suffix):
            raise ValueError(f"cannot parse Singular suffix: {term}")
        expression += monomial
    return sp.Poly(expression, *variables, modulus=PRIME)


def singular(polynomial: sp.Poly | sp.Expr, variables=None) -> str:
    value = polynomial if isinstance(polynomial, sp.Poly) else sp.Poly(
        polynomial, *(variables or ()), modulus=PRIME
    )
    return str(value.as_expr()).replace("**", "^")


def summary(polynomial: sp.Poly) -> dict:
    text = str(polynomial.as_expr())
    return {
        "degree": None if polynomial.is_zero else int(polynomial.total_degree()),
        "degrees": (
            [None] * len(polynomial.gens) if polynomial.is_zero else
            [int(polynomial.degree(value)) for value in polynomial.gens]
        ),
        "terms": len(polynomial.terms()),
        "sha256": hashlib.sha256(text.encode()).hexdigest(),
        "expression": text,
    }


def run_singular(program: str, timeout: int = 240) -> str:
    process = subprocess.run(
        ["Singular", "--quiet"], input=program, capture_output=True,
        text=True, timeout=timeout,
    )
    if process.returncode or "?" in process.stdout or "END" not in process.stdout:
        raise RuntimeError(
            f"Singular failed ({process.returncode}):\n{process.stdout[-4000:]}\n"
            f"{process.stderr[-2000:]}"
        )
    return process.stdout


def integer(stdout: str, label: str) -> int:
    match = re.search(rf"(?:^|\n){label}=(-?\d+)", stdout)
    if not match:
        raise RuntimeError(f"missing Singular integer {label}")
    return int(match.group(1))


def marked_rows(stdout: str, prefix: str, count: int) -> list[str]:
    rows = []
    for index in range(1, count + 1):
        match = re.search(
            rf"{prefix}={index},BEGIN\n(.*?)\n{prefix}={index},END",
            stdout, re.DOTALL,
        )
        if not match:
            raise RuntimeError(f"missing Singular row {prefix}={index}")
        rows.append("".join(match.group(1).split()))
    return rows


def load_basis(pilot_path: Path) -> tuple[list[sp.Poly], dict]:
    payload = json.loads(pilot_path.read_text())
    rows = [
        row for row in payload["rows"]
        if row["cell"] == CELL and row["pivot"] == PIVOT
        and row["epsilon"] == list(EPSILON)
    ]
    if len(rows) != 1 or rows[0]["status"] != "COMPLETE":
        raise RuntimeError("missing unique complete cell-11 pivot-1 pilot row")
    variables = sp.symbols("c b t r")
    basis = [
        parse_singular(item["expression"], variables)
        for item in rows[0]["lex_basis"]
    ]
    if len(basis) != 8:
        raise RuntimeError("expected eight pilot lex-basis equations")
    return basis, rows[0]


def tower_chart(basis: list[sp.Poly], c_row: int) -> dict:
    c, b, t, r = basis[0].gens
    base = sp.Poly(basis[0].as_expr(), t, r, modulus=PRIME)
    b_relation = basis[1]
    b_univariate = sp.Poly(b_relation.as_expr(), b)
    if b_univariate.degree() != 2:
        raise RuntimeError("expected quadratic b relation")
    b_leading = sp.Poly(
        b_univariate.coeff_monomial(b**2), t, r, modulus=PRIME
    )
    c_relation = basis[c_row - 1]
    c_univariate = sp.Poly(c_relation.as_expr(), c)
    if c_univariate.degree() != 1:
        raise RuntimeError("expected linear c relation")
    c_leading = sp.Poly(
        c_univariate.coeff_monomial(c), b, t, r, modulus=PRIME
    )
    definitions = "\n".join(
        f"poly k{index}={singular(value)};"
        for index, value in enumerate(basis, start=1)
    )
    reductions = "\n".join(
        f'print("ROW={index},BEGIN"); print(reduce(k{index},Q)); '
        f'print("ROW={index},END");'
        for index in range(1, 9)
    )
    program = f"""
ring R={PRIME},(z,c,b,t,r),dp;
option(redSB);
{definitions}
poly frel={singular(base)};
poly brel={singular(b_relation)};
poly bden={singular(b_leading)};
poly crel={singular(c_relation)};
poly cden={singular(c_leading)};
poly H={GUARD};
ideal K=k1,k2,k3,k4,k5,k6,k7,k8,z*H-1; K=slimgb(K);
ideal Q=frel,brel,crel,z*H*bden*cden-1; Q=slimgb(Q);
ideal JB=K,bden; JB=slimgb(JB);
ideal JC=K,cden; JC=slimgb(JC);
print("BEGIN");
print("KDIM="+string(dim(K))); print("KSIZE="+string(size(K)));
print("QDIM="+string(dim(Q))); print("QSIZE="+string(size(Q)));
print("JBDIM="+string(dim(JB))); print("JBSIZE="+string(size(JB)));
print("JCDIM="+string(dim(JC))); print("JCSIZE="+string(size(JC)));
{reductions}
print("END"); quit;
"""
    stdout = run_singular(program)
    remainders = marked_rows(stdout, "ROW", 8)
    return {
        "c_row": c_row,
        "base": summary(base),
        "b_relation": summary(b_relation),
        "b_leading": summary(b_leading),
        "c_relation": summary(c_relation),
        "c_leading": summary(c_leading),
        "kernel_dimension": integer(stdout, "KDIM"),
        "kernel_basis_size": integer(stdout, "KSIZE"),
        "tower_dimension": integer(stdout, "QDIM"),
        "tower_basis_size": integer(stdout, "QSIZE"),
        "b_boundary_dimension": integer(stdout, "JBDIM"),
        "b_boundary_basis_size": integer(stdout, "JBSIZE"),
        "c_boundary_dimension": integer(stdout, "JCDIM"),
        "c_boundary_basis_size": integer(stdout, "JCSIZE"),
        "remainders": remainders,
        "exact": remainders == ["0"] * 8,
        "program_sha256": hashlib.sha256(program.encode()).hexdigest(),
    }


def lex_boundaries(basis: list[sp.Poly], c_row: int = 5) -> dict[str, list[str]]:
    c, b, t, r = basis[0].gens
    b_relation = basis[1]
    b_poly = sp.Poly(b_relation.as_expr(), b)
    b_leading = sp.Poly(b_poly.coeff_monomial(b**2), t, r, modulus=PRIME)
    c_relation = basis[c_row - 1]
    c_poly = sp.Poly(c_relation.as_expr(), c)
    c_leading = sp.Poly(c_poly.coeff_monomial(c), b, t, r, modulus=PRIME)
    definitions = "\n".join(
        f"poly k{index}={singular(value)};"
        for index, value in enumerate(basis, start=1)
    )
    printer = "\n".join((
        'for (int i=1; i<=size(JB); i++) { print("JB="+string(i)+",BEGIN"); print(JB[i]); print("JB="+string(i)+",END"); }',
        'for (int i=1; i<=size(JC); i++) { print("JC="+string(i)+",BEGIN"); print(JC[i]); print("JC="+string(i)+",END"); }',
    ))
    program = f"""
ring R={PRIME},(z,c,b,t,r),lp;
option(redSB);
{definitions}
poly H={GUARD};
poly bden={singular(b_leading)};
poly cden={singular(c_leading)};
ideal K=k1,k2,k3,k4,k5,k6,k7,k8,z*H-1;
ideal JB=K,bden; JB=std(JB);
ideal JC=K,cden; JC=std(JC);
print("BEGIN"); print("JBSIZE="+string(size(JB))); print("JCSIZE="+string(size(JC)));
{printer}
print("END"); quit;
"""
    stdout = run_singular(program)
    return {
        "b": marked_rows(stdout, "JB", integer(stdout, "JBSIZE")),
        "c": marked_rows(stdout, "JC", integer(stdout, "JCSIZE")),
        "program_sha256": hashlib.sha256(program.encode()).hexdigest(),
    }


def factor_coefficients(poly: sp.Poly) -> list[int]:
    monic = poly.monic()
    return [int(value) % PRIME for value in monic.all_coeffs()]


def analyze_boundary(expressions: list[str]) -> dict:
    z, c, b, t, r = sp.symbols("z c b t r")
    variables = (z, c, b, t, r)
    polynomials = [parse_singular(value, variables) for value in expressions]
    r_candidates = [
        value for value in polynomials
        if value.degree(r) == 4 and all(value.degree(x) == 0 for x in (z, c, b, t))
    ]
    if len(r_candidates) != 1:
        raise RuntimeError("expected one quartic r boundary")
    r_poly = sp.Poly(r_candidates[0].as_expr(), r, modulus=PRIME)
    coefficient, factors = sp.factor_list(r_poly.as_expr(), r, modulus=PRIME)
    factor_rows = []
    roots = []
    for factor, multiplicity in factors:
        value = sp.Poly(factor, r, modulus=PRIME).monic()
        factor_rows.append({
            "degree": int(value.degree()),
            "multiplicity": int(multiplicity),
            "coefficients": factor_coefficients(value),
        })
        if value.degree() == 1:
            roots.extend([(-factor_coefficients(value)[1]) % PRIME] * int(multiplicity))
    if len(roots) != 1 or sorted(row["degree"] for row in factor_rows) != [1, 3]:
        raise RuntimeError("quartic boundary did not split as one linear plus one cubic")
    r_root = roots[0]
    t_candidates = [
        value for value in polynomials
        if value.degree(t) == 1 and all(value.degree(x) == 0 for x in (z, c, b))
    ]
    if len(t_candidates) != 1:
        raise RuntimeError("expected one linear t lift")
    t_poly = sp.Poly(t_candidates[0].as_expr().subs(r, r_root), t, modulus=PRIME)
    t_coefficients = [int(value) % PRIME for value in t_poly.all_coeffs()]
    t_root = (-t_coefficients[1] * pow(t_coefficients[0], -1, PRIME)) % PRIME
    b_candidates = [
        value for value in polynomials
        if value.degree(b) == 2 and all(value.degree(x) == 0 for x in (z, c))
    ]
    if len(b_candidates) != 1:
        raise RuntimeError("expected one quadratic b lift")
    b_poly = sp.Poly(
        b_candidates[0].as_expr().subs({r: r_root, t: t_root}), b,
        modulus=PRIME,
    ).monic()
    b_coefficients = factor_coefficients(b_poly)
    discriminant = (b_coefficients[1] ** 2 - 4 * b_coefficients[2]) % PRIME
    euler = pow(discriminant, (PRIME - 1) // 2, PRIME)
    return {
        "lex_basis": expressions,
        "lex_basis_sha256": hashlib.sha256("\n".join(expressions).encode()).hexdigest(),
        "r_polynomial": factor_coefficients(r_poly),
        "r_factorization": factor_rows,
        "r_deployed_roots": roots,
        "t_lift": t_root,
        "b_polynomial": b_coefficients,
        "b_discriminant": discriminant,
        "b_discriminant_euler": euler,
        "deployed_boundary_empty": euler == PRIME - 1,
    }


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("cell11_common", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load common compiler")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compile_kernel(paths: dict[str, Path], basis: list[sp.Poly]) -> dict:
    module = load_module(paths["common"])
    variables, _, metadata = module.compile_cell(CELL, *EPSILON)
    t, r, c, b = variables
    labels = metadata["labels"]
    products = metadata["products"]
    q_values = metadata["q_values"]
    product_payload = json.loads(paths["product"].read_text())
    product_row = next(row for row in product_payload["rows"] if row["cell"] == CELL)
    raw = tuple(
        sp.Poly(sp.sympify(value), *variables, modulus=PRIME)
        for value in product_row["kernel_cofactor_expressions"]
    )
    product_gcd = functools.reduce(sp.gcd, raw)
    cofactors = []
    for value in raw:
        quotient, remainder = sp.div(value, product_gcd)
        if not remainder.is_zero:
            raise RuntimeError("nonexact product cofactor gcd division")
        cofactors.append(quotient.as_expr())
    pivot_label = labels[PIVOT]
    pivot_scale = sp.expand(pivot_label * (1 - pivot_label))
    a_at_pivot = sp.expand(sum(
        cofactors[index] * pivot_label**index for index in range(3)
    ))
    gamma = sp.expand(q_values[PIVOT] * a_at_pivot)
    kernel = [
        *(sp.expand(pivot_scale * value) for value in cofactors),
        -gamma, gamma,
    ]
    kernel_polys = [sp.Poly(value, *variables, modulus=PRIME) for value in kernel]
    kernel_gcd = functools.reduce(sp.gcd, kernel_polys)
    primitive = []
    for value in kernel_polys:
        quotient, remainder = sp.div(value, kernel_gcd)
        if not remainder.is_zero:
            raise RuntimeError("nonexact final kernel gcd division")
        primitive.append(quotient.as_expr())
    first = next(sp.Poly(value, *variables, modulus=PRIME) for value in primitive if value != 0)
    inverse = pow(int(first.LC()) % PRIME, -1, PRIME)
    primitive = [
        sp.Poly(inverse * value, *variables, modulus=PRIME).as_expr()
        for value in primitive
    ]
    product_rows = [
        [-product, -product * label, -product * label**2,
         1, label, label**2, 0, 0]
        for label, product in zip(labels, products)
    ]
    sum_rows = [
        [q_value, q_value * label, q_value * label**2,
         0, 0, 0, label, label**2]
        for label, q_value in zip(labels, q_values)
    ]
    row_dots = [
        sp.expand(sum(left * right for left, right in zip(row, primitive)))
        for row in [*product_rows, *sum_rows]
    ]
    identically_zero = [
        sp.Poly(value, *variables, modulus=PRIME).is_zero for value in row_dots
    ]
    definitions = "\n".join(
        f"poly k{index}={singular(value)};"
        for index, value in enumerate(basis, start=1)
    )
    row_definitions = "\n".join(
        f"poly v{index}={singular(sp.Poly(value, *variables, modulus=PRIME))};"
        for index, value in enumerate(row_dots)
    )
    reductions = "\n".join(
        f'print("ROW={index + 1},BEGIN"); print(reduce(v{index},G)); '
        f'print("ROW={index + 1},END");'
        for index in range(len(row_dots))
    )
    program = f"""
ring R={PRIME},(z,t,r,c,b),(dp(1),dp(4));
option(redSB);
{definitions}
{row_definitions}
ideal G=k1,k2,k3,k4,k5,k6,k7,k8,z*({GUARD})-1; G=slimgb(G);
print("BEGIN"); print("DIM="+string(dim(G))); print("SIZE="+string(size(G)));
{reductions}
print("END"); quit;
"""
    stdout = run_singular(program)
    remainders = marked_rows(stdout, "ROW", 10)
    return {
        "epsilon": list(EPSILON),
        "pivot": PIVOT,
        "product_kernel_removed_gcd": summary(product_gcd),
        "final_kernel_removed_gcd": summary(kernel_gcd),
        "kernel": [summary(sp.Poly(value, *variables, modulus=PRIME)) for value in primitive],
        "identically_zero_rows": identically_zero,
        "remainders": remainders,
        "all_rows_zero": remainders == ["0"] * 10,
        "common_dimension": integer(stdout, "DIM"),
        "common_basis_size": integer(stdout, "SIZE"),
        "program_sha256": hashlib.sha256(program.encode()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dag-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    paths = source_paths(arguments.dag_root)
    verify_sources(arguments.dag_root, paths)
    basis, pilot_row = load_basis(paths["pilot"])
    charts = [tower_chart(basis, c_row) for c_row in (5, 6, 7)]
    lex = lex_boundaries(basis, 5)
    payload = {
        "schema": "kb-mca-v4-433-1b-cell11-compact-tower-raw-v1",
        "field": PRIME,
        "source_commit": SOURCE_COMMIT,
        "source_sha256": SOURCE_HASHES,
        "pilot_program_sha256": pilot_row["program_sha256"],
        "pilot_quotient_exact": pilot_row["quotient_exact"],
        "charts": charts,
        "selected_c_row": 5,
        "boundaries": {
            "b_leading": analyze_boundary(lex["b"]),
            "c_leading": analyze_boundary(lex["c"]),
            "program_sha256": lex["program_sha256"],
        },
        "kernel": compile_kernel(paths, basis),
    }
    arguments.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "charts": [
            [row["c_row"], row["tower_basis_size"], row["exact"]]
            for row in charts
        ],
        "b_boundary_empty": payload["boundaries"]["b_leading"]["deployed_boundary_empty"],
        "c_boundary_empty": payload["boundaries"]["c_leading"]["deployed_boundary_empty"],
        "kernel_all_rows_zero": payload["kernel"]["all_rows_zero"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
