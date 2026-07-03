#!/usr/bin/env python3
"""E17 Hankel-kernel sparse-support coset-pattern census.

This is an EXPERIMENTAL verifier, not a proof.  It follows the E17/QF.14
evidence request:

* K = F_17 and H = F_17^* with n = 16;
* sample full-rank Hankel row spaces in the low-degree kernel cases that feed
  the Conjecture-F/Hankel termination lane;
* enumerate exact sparse dual supports of size <= 3;
* classify every recorded support against the nontrivial coset-union lattice.

A support is counted only when the Hankel row space intersects the span of the
corresponding evaluation vectors with all support coefficients nonzero.  Thus a
support is exact; zero-coefficient supersets are not counted as new supports.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


P = 17
N = 16
GENERATOR = 3
MAX_SUPPORT = 3
OUTPUT = Path(
    "experimental/data/certificates/hankel-kernel-coset-census/"
    "hankel_kernel_coset_census_f17_n16.json"
)


@dataclass(frozen=True)
class HankelCase:
    name: str
    degree: int
    rows: int
    samples: int
    seed: int


CASES = (
    HankelCase("sampled_hankel_kernel_lines_j3_t2", 3, 2, 128, 202607031732),
    HankelCase("sampled_hankel_kernel_planes_j4_t2", 4, 2, 256, 202607031742),
    HankelCase("sampled_hankel_kernel_planes_j5_t3", 5, 3, 512, 202607031753),
)


def inv(value: int) -> int:
    return pow(value % P, -1, P)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def rank_mod_p(rows: list[tuple[int, ...]], width: int) -> int:
    work = [[entry % P for entry in row[:width]] for row in rows]
    rank = 0
    for col in range(width):
        pivot = None
        for row in range(rank, len(work)):
            if work[row][col] % P:
                pivot = row
                break
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = inv(work[rank][col])
        work[rank] = [(scale * entry) % P for entry in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][col] % P:
                multiple = work[row][col]
                work[row] = [
                    (work[row][idx] - multiple * work[rank][idx]) % P
                    for idx in range(width)
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def nullspace_basis(rows: list[tuple[int, ...]], width: int) -> list[tuple[int, ...]]:
    work = [[entry % P for entry in row[:width]] for row in rows]
    rank = 0
    pivots: list[int] = []
    for col in range(width):
        pivot = None
        for row in range(rank, len(work)):
            if work[row][col] % P:
                pivot = row
                break
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = inv(work[rank][col])
        work[rank] = [(scale * entry) % P for entry in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][col] % P:
                multiple = work[row][col]
                work[row] = [
                    (work[row][idx] - multiple * work[rank][idx]) % P
                    for idx in range(width)
                ]
        pivots.append(col)
        rank += 1
        if rank == len(work):
            break

    pivot_set = set(pivots)
    basis: list[tuple[int, ...]] = []
    for free in range(width):
        if free in pivot_set:
            continue
        vector = [0] * width
        vector[free] = 1
        for row, pivot_col in enumerate(pivots):
            vector[pivot_col] = (-work[row][free]) % P
        basis.append(tuple(vector))
    return basis


def projective_points(width: int):
    for first in range(width):
        prefix = (0,) * first + (1,)
        tail_width = width - first - 1
        for tail in itertools.product(range(P), repeat=tail_width):
            yield prefix + tail


def eval_vector(x: int, degree: int) -> tuple[int, ...]:
    return tuple(pow(x, exponent, P) for exponent in range(degree + 1))


def domain_values() -> list[int]:
    if pow(GENERATOR, N, P) != 1 or any(
        pow(GENERATOR, exponent, P) == 1 for exponent in range(1, N)
    ):
        raise AssertionError("GENERATOR is not primitive for F_17^*")
    values = [pow(GENERATOR, exponent, P) for exponent in range(N)]
    return values


def random_hankel_rows(
    rng: random.Random, degree: int, rows: int
) -> list[tuple[int, ...]]:
    syndrome = [rng.randrange(P) for _ in range(degree + rows)]
    return [
        tuple(syndrome[row + col] for col in range(degree + 1))
        for row in range(rows)
    ]


def coset_union_orders(support_exponents: tuple[int, ...]) -> list[int]:
    support = set(support_exponents)
    orders: list[int] = []
    for order in range(2, N + 1):
        if N % order or len(support) % order:
            continue
        step = N // order
        if all(((exponent + step) % N) in support for exponent in support):
            orders.append(order)
    return orders


def support_class(support_exponents: tuple[int, ...]) -> tuple[str, list[int]]:
    orders = coset_union_orders(support_exponents)
    if len(support_exponents) == 1:
        return "singleton_common_root", orders
    if orders:
        return "nontrivial_coset_union", orders
    return "noncoset", orders


def exact_support_witness(
    rowspace: list[tuple[int, ...]],
    degree: int,
    support_values: tuple[int, ...],
) -> dict[str, Any] | None:
    """Return one exact-support relation, if one exists.

    The returned coefficients satisfy

        sum_i row_coefficients[i] * row_i
          = sum_s support_coefficients[s] * eval(support_values[s]).

    All support coefficients are nonzero.
    """
    width = degree + 1
    row_rank = rank_mod_p(rowspace, width)
    evals = [eval_vector(value, degree) for value in support_values]
    if rank_mod_p(evals, width) != len(evals):
        raise AssertionError("support evaluation vectors should be independent")

    if rank_mod_p(rowspace + evals, width) == row_rank + len(evals):
        return None

    equations = []
    for col in range(width):
        equations.append(
            tuple(
                [row[col] for row in rowspace]
                + [(-evaluation[col]) % P for evaluation in evals]
            )
        )

    variable_count = len(rowspace) + len(evals)
    basis = nullspace_basis(equations, variable_count)
    if not basis:
        return None

    for coeffs in projective_points(len(basis)):
        solution = [0] * variable_count
        for coeff, basis_vector in zip(coeffs, basis):
            if coeff:
                for idx, value in enumerate(basis_vector):
                    solution[idx] = (solution[idx] + coeff * value) % P
        support_coefficients = solution[len(rowspace) :]
        if not all(support_coefficients):
            continue
        dual_vector = [0] * width
        for coeff, row in zip(solution[: len(rowspace)], rowspace):
            if coeff:
                for idx, value in enumerate(row):
                    dual_vector[idx] = (dual_vector[idx] + coeff * value) % P
        return {
            "row_coefficients": solution[: len(rowspace)],
            "support_coefficients": support_coefficients,
            "dual_vector": dual_vector,
        }

    return None


def record_example(
    examples: dict[str, dict[str, Any]],
    class_name: str,
    support_size: int,
    rowspace: list[tuple[int, ...]],
    support_exponents: tuple[int, ...],
    support_values: tuple[int, ...],
    orders: list[int],
    witness: dict[str, Any],
) -> None:
    key = f"{support_size}:{class_name}"
    if key in examples:
        return
    examples[key] = {
        "support_size": support_size,
        "class": class_name,
        "support_exponents": list(support_exponents),
        "support_values": list(support_values),
        "nontrivial_coset_union_orders": orders,
        "hankel_rows": [list(row) for row in rowspace],
        "relation": witness,
    }


def scan_case(case: HankelCase, domain: list[int]) -> dict[str, Any]:
    rng = random.Random(case.seed)
    attempts = 0
    accepted = 0
    class_counts: Counter[str] = Counter()
    counts_by_size: dict[str, Counter[str]] = {
        str(size): Counter() for size in range(1, MAX_SUPPORT + 1)
    }
    rowspaces_with_noncoset = 0
    noncoset_min_support: int | None = None
    examples: dict[str, dict[str, Any]] = {}

    while accepted < case.samples:
        attempts += 1
        rowspace = random_hankel_rows(rng, case.degree, case.rows)
        if rank_mod_p(rowspace, case.degree + 1) != case.rows:
            continue
        accepted += 1
        saw_noncoset = False
        for support_size in range(1, MAX_SUPPORT + 1):
            for support_exponents in itertools.combinations(range(N), support_size):
                support_values = tuple(domain[exponent] for exponent in support_exponents)
                witness = exact_support_witness(rowspace, case.degree, support_values)
                if witness is None:
                    continue
                class_name, orders = support_class(support_exponents)
                class_counts[class_name] += 1
                counts_by_size[str(support_size)][class_name] += 1
                if class_name == "noncoset":
                    saw_noncoset = True
                    noncoset_min_support = (
                        support_size
                        if noncoset_min_support is None
                        else min(noncoset_min_support, support_size)
                    )
                record_example(
                    examples,
                    class_name,
                    support_size,
                    rowspace,
                    support_exponents,
                    support_values,
                    orders,
                    witness,
                )
        if saw_noncoset:
            rowspaces_with_noncoset += 1

    noncoset_support_count = class_counts["noncoset"]
    return {
        "name": case.name,
        "degree": case.degree,
        "hankel_rows": case.rows,
        "kernel_vector_dimension": case.degree + 1 - case.rows,
        "kernel_projective_dimension": case.degree - case.rows,
        "seed": case.seed,
        "accepted_full_rank_rowspaces": accepted,
        "attempts": attempts,
        "max_sparse_support_tested": MAX_SUPPORT,
        "support_class_counts": dict(sorted(class_counts.items())),
        "support_class_counts_by_size": {
            size: dict(sorted(counter.items()))
            for size, counter in sorted(counts_by_size.items())
        },
        "rowspaces_with_noncoset_support": rowspaces_with_noncoset,
        "noncoset_support_count": noncoset_support_count,
        "noncoset_min_support_size": noncoset_min_support,
        "examples": dict(sorted(examples.items())),
    }


def choose_counterexample(cases: list[dict[str, Any]]) -> dict[str, Any] | None:
    for preferred in ("sampled_hankel_kernel_planes_j5_t3",):
        for case in cases:
            if case["name"] != preferred:
                continue
            for key in sorted(case["examples"]):
                example = case["examples"][key]
                if example["class"] == "noncoset":
                    return {"case": case["name"], **example}
    for case in cases:
        for key in sorted(case["examples"]):
            example = case["examples"][key]
            if example["class"] == "noncoset":
                return {"case": case["name"], **example}
    return None


def build_certificate() -> dict[str, Any]:
    domain = domain_values()
    cases = [scan_case(case, domain) for case in CASES]
    counterexample = choose_counterexample(cases)
    noncoset_found = counterexample is not None
    outcome = (
        "NONCOSET_SPARSE_SUPPORT_FOUND__COSET_UNION_PREDICTION_FALSE"
        if noncoset_found
        else "ALL_RECORDED_SUPPORTS_COSET_UNIONS_OR_SINGLETONS"
    )
    payload: dict[str, Any] = {
        "schema": "hankel_kernel_coset_census.v1",
        "roadmap_task": "E17 / QF.14 / f_termination_hankel",
        "status": "COUNTEREXAMPLE" if noncoset_found else "EXPERIMENTAL_EVIDENCE",
        "field": {
            "p": P,
            "domain": "F_17^*",
            "n": N,
            "primitive_generator": GENERATOR,
            "domain_by_exponent": domain,
        },
        "object": (
            "full-rank Hankel rowspaces R in the dual coefficient space; "
            "a support S is counted when R intersects span{ev(x): x in S} "
            "with every coefficient on S nonzero"
        ),
        "max_sparse_support_tested": MAX_SUPPORT,
        "cases": cases,
        "interpretation": {
            "outcome": outcome,
            "noncoset_support_found": noncoset_found,
            "counterexample": counterexample,
            "qf14_consequence": (
                "The divisor-poset-only termination prediction is false in "
                "the tested Hankel-kernel toy cases.  The descent should use "
                "the general sparse-support lattice branch unless additional "
                "hypotheses exclude these supports."
                if noncoset_found
                else "No sampled obstruction to the coset-union prediction was recorded."
            ),
        },
        "nonclaims": [
            "does not prove a theorem about all Hankel kernels",
            "does not enumerate all syndrome sequences or all rowspaces",
            "does not test sparse support size larger than 3",
            "singletons are recorded as common-root/tangent supports, not as coset-union failures",
        ],
        "script_sha256": sha256_text(Path(__file__).read_text()),
    }
    normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["payload_sha256"] = sha256_text(normalized)
    return payload


def print_summary(certificate: dict[str, Any]) -> None:
    print(certificate["schema"])
    print(certificate["interpretation"]["outcome"])
    for case in certificate["cases"]:
        print(
            f"{case['name']}: accepted={case['accepted_full_rank_rowspaces']} "
            f"noncoset={case['noncoset_support_count']} "
            f"min_noncoset={case['noncoset_min_support_size']}"
        )
        print(f"  classes={case['support_class_counts']}")
    counterexample = certificate["interpretation"]["counterexample"]
    if counterexample:
        print("counterexample:")
        print(
            f"  case={counterexample['case']} "
            f"support_exponents={counterexample['support_exponents']} "
            f"support_values={counterexample['support_values']}"
        )
        print(f"  hankel_rows={counterexample['hankel_rows']}")
        print(f"  relation={counterexample['relation']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="write the certificate JSON")
    parser.add_argument("--check", type=Path, help="check an existing certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    if args.check:
        existing = json.loads(args.check.read_text())
        if existing != certificate:
            raise SystemExit(f"certificate mismatch: {args.check}")
    if not args.emit and not args.check:
        print_summary(certificate)


if __name__ == "__main__":
    main()
