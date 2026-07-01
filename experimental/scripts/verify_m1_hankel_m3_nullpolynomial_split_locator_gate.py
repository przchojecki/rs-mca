#!/usr/bin/env python3
"""Verify the M3 null-polynomial and split-locator gate."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (  # noqa: E402
    Field,
    K,
    MODULUS,
    N,
    P,
    SUBGROUP_ORDER,
)


SCHEMA_VERSION = "f17-32-m3-nullpolynomial-split-locator-gate-v1"
Q_LINE = 17**32
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
RANK_DROP_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-regular-root-rank-drop/"
    "f17_32_n512_k256_m3_m5_regular_root_rank_drop.json"
)
FINITE_AFFINE_KERNEL_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-finite-affine-kernel-chart/"
    "f17_32_n512_k256_m3_m5_finite_affine_kernel_chart.json"
)
RANK_NODE_DICHOTOMY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank-node-dichotomy/"
    "f17_32_n512_k256_m3_rank_node_dichotomy.json"
)


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def hash_value(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def trim(poly: list[int], prime: int) -> list[int]:
    out = [entry % prime for entry in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_mul(left: list[int], right: list[int], prime: int) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, left_i in enumerate(left):
        for j, right_j in enumerate(right):
            out[i + j] = (out[i + j] + left_i * right_j) % prime
    return trim(out, prime)


def poly_divmod(numerator: list[int], denominator: list[int], prime: int) -> tuple[list[int], list[int]]:
    work = trim(numerator, prime)
    divisor = trim(denominator, prime)
    require(divisor != [0], "division by zero polynomial")
    quotient = [0] * max(1, len(work) - len(divisor) + 1)
    while len(work) >= len(divisor) and work != [0]:
        coeff = work[-1] * pow(divisor[-1], -1, prime) % prime
        shift = len(work) - len(divisor)
        quotient[shift] = coeff
        for index, term in enumerate(divisor):
            work[shift + index] = (work[shift + index] - coeff * term) % prime
        work = trim(work, prime)
    return trim(quotient, prime), work


def poly_eval(poly: list[int], value: int, prime: int) -> int:
    total = 0
    power = 1
    for coeff in poly:
        total = (total + coeff * power) % prime
        power = power * value % prime
    return total


def mat_vec(matrix: list[list[int]], vector: list[int], prime: int) -> list[int]:
    return [
        sum(row[col] * vector[col] for col in range(len(vector))) % prime
        for row in matrix
    ]


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    rank = 0
    rows = len(work)
    cols = len(work[0]) if rows else 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if work[row][col] % prime:
                pivot = row
                break
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inv = pow(work[rank][col], -1, prime)
        work[rank] = [entry * inv % prime for entry in work[rank]]
        for row in range(rows):
            if row == rank or work[row][col] == 0:
                continue
            factor = work[row][col]
            work[row] = [
                (work[row][entry_col] - factor * work[rank][entry_col]) % prime
                for entry_col in range(cols)
            ]
        rank += 1
    return rank


def locator_poly(roots: list[int], prime: int) -> list[int]:
    out = [1]
    for root in roots:
        out = poly_mul(out, [(-root) % prime, 1], prime)
    return out


def sanity_checks() -> list[dict[str, Any]]:
    prime = 17
    domain_poly = [(-1) % prime] + [0] * 15 + [1]

    split_locator = locator_poly([1, 2], prime)
    split_syndrome = [1, 0, 15, 11, 3]
    split_matrix = [
        split_syndrome[row : row + 3]
        for row in range(3)
    ]
    _quotient, split_remainder = poly_divmod(domain_poly, split_locator, prime)
    require(split_remainder == [0], "split locator does not divide domain polynomial")
    require(mat_vec(split_matrix, split_locator, prime) == [0, 0, 0], "split recurrence failed")
    require(rank_mod(split_matrix, prime) == 2, "split sanity rank mismatch")

    direction = [1, 0, 0, 0, 0]
    direction_matrix = [direction[row : row + 3] for row in range(3)]
    require(mat_vec(direction_matrix, split_locator, prime) == [2, 0, 0], "noncontainment sanity failed")

    ambient_only_locator = [0, 0, 1]
    ambient_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 0]]
    _quotient, ambient_remainder = poly_divmod(domain_poly, ambient_only_locator, prime)
    require(ambient_remainder != [0], "ambient-only locator unexpectedly divides domain")
    require(mat_vec(ambient_matrix, ambient_only_locator, prime) == [0, 0, 0], "ambient recurrence failed")
    require(rank_mod(ambient_matrix, prime) == 2, "ambient sanity rank mismatch")

    return [
        {
            "prime": prime,
            "domain": "F_17^* roots of X^16-1",
            "split_locator_low_to_high": split_locator,
            "split_locator_divides_domain_polynomial": True,
            "hankel_recurrence_values": mat_vec(split_matrix, split_locator, prime),
            "direction_recurrence_values": mat_vec(direction_matrix, split_locator, prime),
            "result": "split locator can pass the domain and noncontainment gates",
        },
        {
            "prime": prime,
            "ambient_kernel_vector_low_to_high": ambient_only_locator,
            "ambient_kernel_divides_domain_polynomial": False,
            "hankel_recurrence_values": mat_vec(ambient_matrix, ambient_only_locator, prime),
            "result": "ambient Hankel rank drop can overcount split-domain locators",
        },
    ]


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "null_polynomial_coefficients": j_value + 1,
        "split_locator_degree_required": j_value,
        "hankel_recurrence_equations": t_value,
        "maximal_row_set_count": comb(t_value, j_value + 1),
        "regular_overdetermined": t_value >= j_value + 1,
    }


def check_windows(data_by_name: dict[str, dict[str, Any]]) -> None:
    for name, data in data_by_name.items():
        require(data["row"]["n"] == N, f"{name} n mismatch")
        require(data["row"]["k"] == K, f"{name} k mismatch")
        require(data["window"]["A_min"] == A_MIN, f"{name} A_min mismatch")
        require(data["window"]["A_max"] == A_MAX, f"{name} A_max mismatch")


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    rank_drop = load_json(RANK_DROP_REF)
    finite_kernel = load_json(FINITE_AFFINE_KERNEL_REF)
    rank_node = load_json(RANK_NODE_DICHOTOMY_REF)

    require(descriptor["schema_version"] == "f17-32-hankel-row-descriptor-v1", "descriptor schema mismatch")
    require(rank_drop["schema_version"] == "f17-32-m3-m5-regular-root-rank-drop-v1", "rank-drop schema mismatch")
    require(finite_kernel["schema_version"] == "f17-32-m3-m5-finite-affine-kernel-chart-v1", "finite-kernel schema mismatch")
    require(rank_node["schema_version"] == "f17-32-m3-rank-node-dichotomy-v1", "rank-node schema mismatch")

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    check_windows({"rank_drop": rank_drop, "finite_kernel": finite_kernel, "rank_node": rank_node})
    require(rank_drop["summary"]["nonsingular_rank_drop_implies_regular_root"], "rank-drop converse missing")
    require(finite_kernel["summary"]["max_contribution_per_unfiltered_root"] == 1, "finite-kernel root contribution mismatch")

    domain = descriptor["domain"]["domain_encodings"]
    require(len(domain) == SUBGROUP_ORDER == N, "domain size mismatch")
    require(len(set(domain)) == N, "domain is not distinct")
    require(field.encode(field.zero) not in domain, "zero belongs to domain")
    generator = field.decode(descriptor["domain"]["generator_encoding"])
    powers = []
    current = field.one
    for _ in range(N):
        powers.append(field.encode(current))
        current = field.mul(current, generator)
    require(powers == domain, "domain is not the recorded generator power list")
    require(current == field.one, "generator does not close after 512 powers")
    require(field.pow(generator, N // 2) != field.one, "generator order is not exact")
    require(N % P != 0, "domain polynomial derivative vanishes identically")
    require(field.pow(field.zero, N) != field.one, "zero is a domain root")

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    total_row_sets = sum(record["maximal_row_set_count"] for record in records)
    require(total_row_sets == rank_drop["window"]["all_row_set_total"], "rank-drop row-set total mismatch")
    require(total_row_sets == finite_kernel["window"]["all_row_set_total"], "finite-kernel row-set total mismatch")
    require(all(record["regular_overdetermined"] for record in records), "window not regular")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "M3 finite-root null-polynomial and split-locator gate",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "q_line": Q_LINE,
            "domain_hash": descriptor["row"]["domain_hash"],
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            "regular_root_rank_drop": {"ref": RANK_DROP_REF, "sha256": sha256_file(RANK_DROP_REF)},
            "finite_affine_kernel_chart": {
                "ref": FINITE_AFFINE_KERNEL_REF,
                "sha256": sha256_file(FINITE_AFFINE_KERNEL_REF),
            },
            "rank_node_dichotomy": {
                "ref": RANK_NODE_DICHOTOMY_REF,
                "sha256": sha256_file(RANK_NODE_DICHOTOMY_REF),
            },
        },
        "domain_locator_gate": {
            "domain_polynomial": "X^512 - 1",
            "derivative": "512 X^511 = 2 X^511 in characteristic 17",
            "squarefree": True,
            "root_set": "the recorded order-512 subgroup H",
            "split_locator_criterion": (
                "A monic degree-j polynomial is the locator of a j-subset of H "
                "iff it divides X^512-1."
            ),
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "all_row_set_total": total_row_sets,
            "j_min": min(record["j"] for record in records),
            "j_max": max(record["j"] for record in records),
        },
        "theorem": {
            "null_polynomial_equivalence": (
                "For a finite slope z and s_m(z)=u_m+zv_m, "
                "rank H_{t,j}(s(z))<=j iff there is a nonzero polynomial "
                "L(X)=ell_0+...+ell_j X^j such that "
                "sum_{b=0}^j s_{a+b}(z) ell_b=0 for every 0<=a<t."
            ),
            "regular_root_interpretation": (
                "In a nonsingular regular bucket, the v10 finite canonical roots "
                "are exactly the finite slopes admitting such a nonzero ambient "
                "null-polynomial."
            ),
            "split_locator_gate": (
                "An ambient null-polynomial gives an exact-A split locator only "
                "after normalization to a monic degree-j divisor of X^512-1."
            ),
            "noncontainment_gate": (
                "The support-wise finite-affine noncontainment condition is "
                "H_{t,j}(v) ell != 0.  If H(v)ell=0 as well as "
                "H(u+zv)ell=0, then also H(u)ell=0 and the witness is in the "
                "same-support contained branch."
            ),
            "safe_upper_bound": (
                "Therefore an ambient regular root table is a safe upper bound "
                "for split-locator bad slopes, and future packets may filter "
                "listed roots by the divisor and noncontainment gates."
            ),
            "certificate_payload": [
                "finite slope encoding z",
                "nonzero kernel vector ell for H(u+zv)",
                "normalization degree of L(X)",
                "remainder of L(X) against X^512-1, or divisor proof",
                "the recurrence vector H(u+zv)ell",
                "the noncontainment vector H(v)ell",
            ],
        },
        "agreement_records": records,
        "sanity_checks": sanity_checks(),
        "field_audit": {
            "domain_size": len(domain),
            "domain_hash": hash_value(domain),
            "generator_encoding": descriptor["domain"]["generator_encoding"],
            "generator_exact_order": N,
            "domain_polynomial_derivative_coefficient_mod_17": N % P,
            "x_512_minus_1_squarefree": True,
        },
        "summary": {
            "agreement_count": len(records),
            "null_polynomial_gate_available": True,
            "split_locator_gate_available": True,
            "ambient_root_table_is_safe_upper_bound": True,
            "root_filter_max_contribution_per_unfiltered_root": 1,
        },
        "checks": [
            "dependency schemas and windows match the F_17^32 M3 regular window",
            "the recorded domain is the exact order-512 subgroup generated in the row descriptor",
            "X^512-1 is squarefree in characteristic 17",
            "monic degree-j divisors of X^512-1 are exactly split squarefree j-subgroup locators",
            "rank-drop and finite-affine kernel dependencies expose the required root and noncontainment gates",
            "sanity examples distinguish ambient null-polynomials from split-domain locators",
        ],
        "nonclaims": [
            "does not compute an arbitrary-row finite root table",
            "does not prove that every ambient root has a split locator",
            "does not perform quotient, tangent, extension, or subfield subtraction",
            "does not close singular buckets without root tables or pivot eliminants",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"null-polynomial split-locator certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    print("F_17^32 M3 null-polynomial split-locator gate")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, j={j_min}..{j_max}".format(
            **window
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check)
    print_summary(certificate)


if __name__ == "__main__":
    main()
