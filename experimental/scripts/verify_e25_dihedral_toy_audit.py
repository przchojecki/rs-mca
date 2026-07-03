#!/usr/bin/env python3
"""Verify the E25 toy dihedral/palindromic locator audit.

This is a small exact packet for the E25 dihedral audit.  It works on the
multiplicative row ``mu_16`` over ``F_17`` and ``F_97`` at the toy rate
``k=8``.  The checker has two parts:

1. every inverse-pair support in the audited agreement sizes has a locator of
   the form ``X^h q(X + X^-1)`` (with the expected ``X^2-1`` fixed-branch
   factor when both fixed points ``+-1`` are present);
2. for Chebyshev-character basis lines ``T_e + z T_f``, the finite alignment
   systems on those supports have no residual class outside the tangent,
   cyclic-quotient, or dihedral/antipodal ledgers.

The packet is intentionally toy/local.  It does not enumerate all projective
lines in the full dihedral word space and does not run the M5 prize-row chart
machinery.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / (
    "experimental/data/certificates/e25-dihedral-toy-audit/"
    "e25_dihedral_toy_audit.json"
)

SCHEMA_VERSION = "e25-dihedral-toy-audit-v1"
TASK_ID = "E25"
DAG_NODES = ["payment_completeness", "dihedral_quotient_stratum", "zone_b"]
N = 16
K = 8
AGREEMENTS = (10, 12, 14)
PRIMES = (17, 97)

Poly = list[int]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    remaining = value
    trial = 2
    while trial * trial <= remaining:
        if remaining % trial == 0:
            factors.append(trial)
            while remaining % trial == 0:
                remaining //= trial
        trial += 1 if trial == 2 else 2
    if remaining > 1:
        factors.append(remaining)
    return factors


def primitive_root(p: int) -> int:
    factors = prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for F_{p}")


def mu_16_generator(p: int) -> int:
    require((p - 1) % N == 0, f"mu_16 must sit in F_{p}")
    return pow(primitive_root(p), (p - 1) // N, p)


def domain_values(p: int) -> tuple[int, ...]:
    generator = mu_16_generator(p)
    values = []
    x = 1
    for _ in range(N):
        values.append(x)
        x = x * generator % p
    require(x == 1 and len(set(values)) == N, "domain generator does not have order 16")
    return tuple(values)


def poly_mul(a: Poly, b: Poly, p: int) -> Poly:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return poly_trim(out, p)


def poly_trim(poly: Poly, p: int) -> Poly:
    out = [coefficient % p for coefficient in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_eval(poly: Poly, x: int, p: int) -> int:
    result = 0
    for coefficient in reversed(poly):
        result = (result * x + coefficient) % p
    return result


def locator_poly(roots: Iterable[int], p: int) -> Poly:
    out = [1]
    for root in roots:
        out = poly_mul(out, [(-root) % p, 1], p)
    return out


def quotient_poly(traces: Iterable[int], p: int) -> Poly:
    out = [1]
    for trace in traces:
        out = poly_mul(out, [(-trace) % p, 1], p)
    return out


def chebyshev_lift(q_poly: Poly, h: int, p: int) -> Poly:
    """Return ``X^h q(X + X^-1)`` as an ordinary polynomial."""

    out = [0] * (2 * h + 1)
    for r, coefficient in enumerate(q_poly):
        for a in range(r + 1):
            degree = h - r + 2 * a
            out[degree] = (out[degree] + coefficient * math.comb(r, a)) % p
    return poly_trim(out, p)


def reciprocal_multiplier(poly: Poly, p: int) -> int:
    """Return c when X^deg L(1/X) = c L(X), or raise if no c exists."""

    degree = len(poly) - 1
    require(poly[-1] == 1, "locator is not monic")
    c = poly[0] % p
    for idx in range(degree + 1):
        if poly[degree - idx] % p != c * poly[idx] % p:
            raise AssertionError(f"locator is not reciprocal up to multiplier {c}")
    return c


def inverse_pairs() -> tuple[tuple[int, int], ...]:
    return tuple((idx, (-idx) % N) for idx in range(1, N // 2))


def support_orbit_type(support: tuple[int, ...]) -> dict[str, Any]:
    support_set = set(support)
    cyclic_stabilizers = [
        shift for shift in range(1, N) if {((idx + shift) % N) for idx in support_set} == support_set
    ]
    reflection_stabilizers = [
        center for center in range(N) if {((center - idx) % N) for idx in support_set} == support_set
    ]
    require(0 in reflection_stabilizers, "support is not inversion-stable")
    if cyclic_stabilizers:
        ledger = "multiplicative_quotient_overlap"
    else:
        ledger = "dihedral_antipodal_only"
    return {
        "ledger": ledger,
        "cyclic_stabilizers": cyclic_stabilizers,
        "reflection_stabilizers": reflection_stabilizers,
    }


@dataclass(frozen=True)
class SupportRecord:
    family: str
    agreement: int
    moving_pair_indices: tuple[int, ...]
    fixed_exponents: tuple[int, ...]
    support_exponents: tuple[int, ...]

    @property
    def h(self) -> int:
        return len(self.moving_pair_indices)


def support_records_for_agreement(agreement: int) -> list[SupportRecord]:
    require(agreement > K and agreement <= N and agreement % 2 == 0, "toy audit uses even A>K")
    pairs = inverse_pairs()
    records: list[SupportRecord] = []

    pure_h = agreement // 2
    if pure_h <= len(pairs):
        for selected in combinations(range(len(pairs)), pure_h):
            support = sorted(idx for pair_idx in selected for idx in pairs[pair_idx])
            records.append(
                SupportRecord(
                    family="moving_inverse_pairs",
                    agreement=agreement,
                    moving_pair_indices=tuple(selected),
                    fixed_exponents=(),
                    support_exponents=tuple(support),
                )
            )

    fixed_h = (agreement - 2) // 2
    if fixed_h >= 0 and fixed_h <= len(pairs):
        for selected in combinations(range(len(pairs)), fixed_h):
            support = sorted([0, N // 2] + [idx for pair_idx in selected for idx in pairs[pair_idx]])
            records.append(
                SupportRecord(
                    family="fixed_branch_pm1",
                    agreement=agreement,
                    moving_pair_indices=tuple(selected),
                    fixed_exponents=(0, N // 2),
                    support_exponents=tuple(support),
                )
            )

    return records


def verify_support_locator(record: SupportRecord, xs: tuple[int, ...], p: int) -> dict[str, Any]:
    pairs = inverse_pairs()
    roots = [xs[idx] for idx in record.support_exponents]
    locator = locator_poly(roots, p)

    quadratic_product = [1]
    traces = []
    for pair_idx in record.moving_pair_indices:
        i, j = pairs[pair_idx]
        trace = (xs[i] + xs[j]) % p
        traces.append(trace)
        quadratic_product = poly_mul(quadratic_product, [1, (-trace) % p, 1], p)
    if record.fixed_exponents:
        quadratic_product = poly_mul(quadratic_product, [(-1) % p, 0, 1], p)
    require(locator == quadratic_product, "locator does not match inverse-pair product")

    q_poly = quotient_poly(traces, p)
    lift = chebyshev_lift(q_poly, record.h, p)
    if record.fixed_exponents:
        lift = poly_mul(lift, [(-1) % p, 0, 1], p)
    require(locator == lift, "locator does not match Chebyshev/dihedral lift")

    multiplier = reciprocal_multiplier(locator, p)
    expected_multiplier = (-1 if record.fixed_exponents else 1) % p
    require(multiplier == expected_multiplier, "reciprocal multiplier mismatch")

    for idx in record.support_exponents:
        require(poly_eval(locator, xs[idx], p) == 0, "locator misses a support root")
    outside_roots = [idx for idx in range(N) if idx not in record.support_exponents and poly_eval(locator, xs[idx], p) == 0]
    require(not outside_roots, "locator has an unexpected mu_16 root")

    orbit = support_orbit_type(record.support_exponents)
    return {
        "family": record.family,
        "agreement": record.agreement,
        "h": record.h,
        "support_exponents": list(record.support_exponents),
        "moving_pair_indices": list(record.moving_pair_indices),
        "fixed_exponents": list(record.fixed_exponents),
        "locator_degree": len(locator) - 1,
        "reciprocal_multiplier": multiplier,
        "dihedral_quotient_degree": len(q_poly) - 1,
        "orbit_ledger": orbit["ledger"],
        "cyclic_stabilizers": orbit["cyclic_stabilizers"],
        "reflection_stabilizers": orbit["reflection_stabilizers"],
    }


def inv(value: int, p: int) -> int:
    return pow(value % p, p - 2, p)


def rref(matrix: list[list[int]], p: int) -> tuple[int, list[int], list[list[int]]]:
    if not matrix:
        return 0, [], []
    rows = [[entry % p for entry in row] for row in matrix]
    row_count = len(rows)
    col_count = len(rows[0])
    pivot_cols: list[int] = []
    pivot_row = 0
    for col in range(col_count):
        pivot = None
        for row in range(pivot_row, row_count):
            if rows[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = inv(rows[pivot_row][col], p)
        rows[pivot_row] = [(entry * scale) % p for entry in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or rows[row][col] == 0:
                continue
            factor = rows[row][col]
            rows[row] = [(entry - factor * base) % p for entry, base in zip(rows[row], rows[pivot_row])]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return len(pivot_cols), pivot_cols, rows


def rank_mod(matrix: list[list[int]], p: int) -> int:
    if not matrix:
        return 0
    return rref(matrix, p)[0]


def nullspace_mod(matrix: list[list[int]], p: int) -> list[list[int]]:
    if not matrix:
        return []
    rank, pivot_cols, reduced = rref(matrix, p)
    del rank
    col_count = len(matrix[0])
    free_cols = [col for col in range(col_count) if col not in pivot_cols]
    basis: list[list[int]] = []
    for free_col in free_cols:
        vector = [0] * col_count
        vector[free_col] = 1
        for row, pivot_col in enumerate(pivot_cols):
            vector[pivot_col] = (-reduced[row][free_col]) % p
        basis.append(vector)
    return basis


@lru_cache(maxsize=None)
def support_constraints(p: int, support: tuple[int, ...], dimension: int) -> tuple[tuple[int, ...], ...]:
    xs = domain_values(p)
    if len(support) <= dimension:
        return ()
    vandermonde_t = [[pow(xs[index], degree, p) for index in support] for degree in range(dimension)]
    return tuple(tuple(row) for row in nullspace_mod(vandermonde_t, p))


def fits_degree(values: tuple[int, ...], support: tuple[int, ...], dimension: int, p: int) -> bool:
    for check in support_constraints(p, support, dimension):
        total = sum(check[pos] * values[index] for pos, index in enumerate(support)) % p
        if total:
            return False
    return True


def chebyshev_character_values(e: int, xs: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((pow(x, e, p) + pow(x, (-e) % N, p)) % p for x in xs)


def vector_add_scaled(u: tuple[int, ...], v: tuple[int, ...], z: int, p: int) -> tuple[int, ...]:
    return tuple((ui + z * vi) % p for ui, vi in zip(u, v))


def vector_space_rank(vectors: list[tuple[int, ...]], p: int) -> int:
    if not vectors:
        return 0
    return rank_mod([list(vector) for vector in vectors], p)


def subspace_dimensions(support: tuple[int, ...], xs: tuple[int, ...], p: int) -> dict[str, int]:
    code_vectors = [
        tuple(pow(xs[index], degree, p) for index in support)
        for degree in range(K)
    ]
    dihedral_vectors = [
        tuple(chebyshev_character_values(e, xs, p)[index] for index in support)
        for e in range(N // 2 + 1)
    ]
    code_dim = vector_space_rank(code_vectors, p)
    dihedral_dim = vector_space_rank(dihedral_vectors, p)
    span_dim = vector_space_rank(code_vectors + dihedral_vectors, p)
    intersection_dim = code_dim + dihedral_dim - span_dim
    return {
        "code_restriction_dim": code_dim,
        "dihedral_word_dim": dihedral_dim,
        "combined_span_dim": span_dim,
        "intersection_dim": intersection_dim,
    }


def solve_basis_line_alignments(
    support: tuple[int, ...],
    orbit_ledger: str,
    xs: tuple[int, ...],
    p: int,
) -> tuple[Counter[str], list[dict[str, Any]]]:
    characters = [chebyshev_character_values(e, xs, p) for e in range(N // 2 + 1)]
    event_counts: Counter[str] = Counter()
    examples: list[dict[str, Any]] = []

    for e, f in combinations(range(N // 2 + 1), 2):
        u = characters[e]
        v = characters[f]
        u_fits = fits_degree(u, support, K, p)
        v_fits = fits_degree(v, support, K, p)
        aligned_slopes = []
        ledger_counts: Counter[str] = Counter()
        for z in range(p):
            if not fits_degree(vector_add_scaled(u, v, z, p), support, K, p):
                continue
            if u_fits and v_fits:
                ledger = "tangent_common_code_line"
            elif z == 0 and u_fits:
                ledger = "tangent_code_endpoint"
            elif orbit_ledger == "multiplicative_quotient_overlap":
                ledger = "multiplicative_quotient_overlap"
            else:
                ledger = "dihedral_antipodal_charge"
            aligned_slopes.append(z)
            ledger_counts[ledger] += 1
            event_counts[ledger] += 1

        if aligned_slopes:
            examples.append(
                {
                    "character_line": [e, f],
                    "support_exponents": list(support),
                    "u_fits_code_on_support": u_fits,
                    "v_fits_code_on_support": v_fits,
                    "aligned_finite_slope_count": len(aligned_slopes),
                    "aligned_finite_slopes_sample": aligned_slopes[:16],
                    "ledger_counts": dict(sorted(ledger_counts.items())),
                }
            )

    return event_counts, examples


def alignment_example_priority(example: dict[str, Any]) -> tuple[int, int, list[int], list[int]]:
    ledger_counts = example["ledger_counts"]
    if "dihedral_antipodal_charge" in ledger_counts:
        priority = 0
    elif "multiplicative_quotient_overlap" in ledger_counts:
        priority = 1
    elif "tangent_common_code_line" in ledger_counts:
        priority = 2
    else:
        priority = 3
    return (
        priority,
        example["aligned_finite_slope_count"],
        example["support_exponents"],
        example["character_line"],
    )


def summarize_counter(counter: Counter[str]) -> dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


def audit_prime(p: int) -> dict[str, Any]:
    xs = domain_values(p)
    support_payloads: list[dict[str, Any]] = []
    support_counts: Counter[str] = Counter()
    orbit_counts: Counter[str] = Counter()
    alignment_counts: Counter[str] = Counter()
    dim_records: list[dict[str, Any]] = []
    examples: list[dict[str, Any]] = []

    for agreement in AGREEMENTS:
        records = support_records_for_agreement(agreement)
        expected = math.comb(7, agreement // 2) + math.comb(7, (agreement - 2) // 2)
        require(len(records) == expected, f"support count drift at A={agreement}")

        for record in records:
            payload = verify_support_locator(record, xs, p)
            support_payloads.append(payload)
            support_counts[f"A={agreement}:{record.family}"] += 1
            orbit_counts[payload["orbit_ledger"]] += 1

            dims = subspace_dimensions(record.support_exponents, xs, p)
            dim_records.append(
                {
                    "agreement": agreement,
                    "family": record.family,
                    "orbit_ledger": payload["orbit_ledger"],
                    **dims,
                }
            )

            counts, local_examples = solve_basis_line_alignments(
                record.support_exponents,
                payload["orbit_ledger"],
                xs,
                p,
            )
            alignment_counts.update(counts)
            examples.extend(local_examples)

    unpaid_after_dihedral = sum(
        count
        for ledger, count in alignment_counts.items()
        if ledger
        not in {
            "tangent_common_code_line",
            "tangent_code_endpoint",
            "multiplicative_quotient_overlap",
            "dihedral_antipodal_charge",
        }
    )
    require(unpaid_after_dihedral == 0, "unexpected unpaid alignment ledger")
    require(orbit_counts["dihedral_antipodal_only"] > 0, "toy audit did not see dihedral-only supports")
    require(alignment_counts["dihedral_antipodal_charge"] > 0, "toy audit did not see dihedral charged alignments")

    dim_summary: Counter[str] = Counter()
    for row in dim_records:
        key = (
            f"A={row['agreement']}:"
            f"C={row['code_restriction_dim']}:"
            f"D={row['dihedral_word_dim']}:"
            f"I={row['intersection_dim']}"
        )
        dim_summary[key] += 1

    return {
        "p": p,
        "domain": {
            "n": N,
            "mu_16_generator": mu_16_generator(p),
            "values_by_exponent": list(xs),
        },
        "row": {"k": K, "agreements": list(AGREEMENTS)},
        "support_summary": {
            "total_supports": len(support_payloads),
            "by_family": summarize_counter(support_counts),
            "by_orbit_ledger": summarize_counter(orbit_counts),
        },
        "alignment_summary": {
            "audited_character_lines_per_support": math.comb(N // 2 + 1, 2),
            "finite_alignment_events_by_ledger": summarize_counter(alignment_counts),
            "unpaid_after_tangent_quotient_dihedral_ledgers": unpaid_after_dihedral,
        },
        "dimension_summary": summarize_counter(dim_summary),
        "support_examples": support_payloads[:12],
        "alignment_examples": sorted(examples, key=alignment_example_priority)[:12],
    }


def build_certificate() -> dict[str, Any]:
    cases = [audit_prime(p) for p in PRIMES]
    for case in cases:
        require(
            case["alignment_summary"]["unpaid_after_tangent_quotient_dihedral_ledgers"] == 0,
            f"unpaid ledger in p={case['p']}",
        )
    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": "TOY_AUDIT / LOCATOR_ABSORBED_BY_DIHEDRAL_LEDGER",
        "task_id": TASK_ID,
        "dag_nodes": DAG_NODES,
        "model": {
            "domain": "multiplicative row mu_16 in F_p",
            "toy_rate": "k/n = 8/16",
            "audited_agreements": list(AGREEMENTS),
            "palindromic_locator_forms": [
                "prod_{i in I}(X^2-(a_i+a_i^-1)X+1) = X^h q(X+X^-1)",
                "(X^2-1) prod_{i in I}(X^2-(a_i+a_i^-1)X+1) for the fixed +-1 branch",
            ],
            "alignment_lines": "all unordered Chebyshev-character basis lines T_e + z T_f, 0 <= e < f <= 8",
        },
        "summary": {
            "primes": list(PRIMES),
            "total_supports_per_prime": sum(
                math.comb(7, agreement // 2) + math.comb(7, (agreement - 2) // 2)
                for agreement in AGREEMENTS
            ),
            "character_lines_per_support": math.comb(N // 2 + 1, 2),
            "unpaid_after_dihedral_ledger_all_cases": sum(
                case["alignment_summary"]["unpaid_after_tangent_quotient_dihedral_ledgers"]
                for case in cases
            ),
            "locator_verdict": (
                "every audited inverse-pair locator is a Chebyshev/dihedral pullback; "
                "fixed +-1 supports carry the expected anti-reciprocal branch factor"
            ),
            "alignment_verdict": (
                "all audited finite Chebyshev-basis-line alignments are charged to "
                "tangent, cyclic-quotient overlap, or dihedral/antipodal ledger"
            ),
        },
        "cases": cases,
        "nonclaims": [
            "does not enumerate all projective lines in the full 9-dimensional dihedral word space",
            "does not run the M5 A=384..426 chart restriction",
            "does not prove global E25 payment completeness by itself",
            "does not audit extension-field rows or non-mu_16 multiplicative rows",
        ],
    }
    payload["payload_sha256"] = sha256_json(payload)
    return payload


def check_certificate(path: Path, expected: dict[str, Any]) -> None:
    actual = json.loads(path.read_text(encoding="utf-8"))
    if actual != expected:
        raise AssertionError(f"certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    print("E25 dihedral toy audit")
    print(f"status: {certificate['status']}")
    summary = certificate["summary"]
    print(
        "supports/prime={total_supports_per_prime}, character-lines/support={character_lines_per_support}, unpaid={unpaid_after_dihedral_ledger_all_cases}".format(
            **summary
        )
    )
    for case in certificate["cases"]:
        alignments = case["alignment_summary"]["finite_alignment_events_by_ledger"]
        print(f"F_{case['p']}: supports={case['support_summary']['total_supports']}, alignments={alignments}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        nargs="?",
        const=OUTPUT,
        type=Path,
        help="write deterministic E25 toy-audit JSON, optionally to PATH",
    )
    parser.add_argument(
        "--check",
        nargs="?",
        const=OUTPUT,
        type=Path,
        help="check deterministic E25 toy-audit JSON, optionally at PATH",
    )
    parser.add_argument("--json", action="store_true", help="print certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check, certificate)
    if args.json:
        print(render(certificate), end="")
        return
    print_summary(certificate)


if __name__ == "__main__":
    main()
